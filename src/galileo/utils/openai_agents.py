import logging
from typing import Any, Union

from agents import (
    AgentSpanData,
    CustomSpanData,
    FunctionSpanData,
    GenerationSpanData,
    GuardrailSpanData,
    HandoffSpanData,
    Span,
    SpanData,
)
from agents.tracing import ResponseSpanData

from galileo.schema.handlers import LANGCHAIN_NODE_TYPE
from galileo.utils.serialization import serialize_to_str

_logger = logging.getLogger(__name__)


def _map_span_type(span_data: SpanData) -> LANGCHAIN_NODE_TYPE:
    """Determine the Galileo span type based on the OpenAI Agent span data."""
    if isinstance(span_data, (GenerationSpanData, ResponseSpanData)):
        return "llm"
    elif isinstance(span_data, (FunctionSpanData, GuardrailSpanData)):
        return "tool"
    elif isinstance(span_data, (AgentSpanData, HandoffSpanData, CustomSpanData)):
        return "workflow"
    else:
        # Default to workflow for unknown or base SpanData types
        _logger.debug(f"Unknown span data type {type(span_data)}, defaulting to workflow.")
        return "workflow"


def _map_span_name(span: Span[Any]) -> str:
    """Determine the name for a given OpenAI Agent span."""
    if name := getattr(span.span_data, "name", None):
        return name
    elif isinstance(span.span_data, GenerationSpanData):
        return "Generation"
    elif isinstance(span.span_data, ResponseSpanData):
        return "Response"
    elif isinstance(span.span_data, HandoffSpanData):
        return f"Handoff: {span.span_data.from_agent} -> {span.span_data.to_agent}"
    elif span.span_data.type:
        return span.span_data.type.capitalize()
    else:
        return "Unknown Span"


def _parse_usage(usage_data: Union[dict, Any, None]) -> dict[str, Union[int, None]]:
    """Safely parse usage data into a standardized dictionary."""
    parsed: dict[str, Union[int, None]] = {"input_tokens": None, "output_tokens": None, "total_tokens": None}
    if usage_data is None:
        return parsed

    usage_dict = {}
    if hasattr(usage_data, "model_dump"):
        try:
            usage_dict = usage_data.model_dump()
        except Exception:
            _logger.debug("Failed to model_dump usage data.", exc_info=True)
            # Fallback for GenerationSpanData usage which is already a dict
            if isinstance(usage_data, dict):
                usage_dict = usage_data
            else:
                return parsed  # Cannot parse
    elif isinstance(usage_data, dict):
        usage_dict = usage_data
    else:
        return parsed  # Cannot parse

    # Prioritize specific keys, fall back to alternatives
    parsed["input_tokens"] = usage_dict.get("input_tokens", usage_dict.get("prompt_tokens"))
    parsed["output_tokens"] = usage_dict.get("output_tokens", usage_dict.get("completion_tokens"))
    parsed["total_tokens"] = usage_dict.get("total_tokens")

    # Ensure values are integers if not None
    for key in parsed:
        if parsed[key] is not None:
            try:
                parsed[key] = int(parsed[key])
            except (ValueError, TypeError):
                _logger.warning(f"Could not convert usage value '{parsed[key]}' for key '{key}' to int.")
                parsed[key] = None  # Reset if conversion fails

    return parsed


def _extract_llm_data(span_data: Union[GenerationSpanData, ResponseSpanData]) -> dict[str, Any]:
    """Extract data specific to LLM spans (Generation, Response)."""
    data: dict[str, Any] = {
        "input": None,
        "output": None,
        "model": None,
        "temperature": None,
        "num_input_tokens": None,
        "num_output_tokens": None,
        "total_tokens": None,
        "metadata": {"gen_ai_system": "openai"},  # Default assumption
        "model_parameters": {},
        "tools": None,
        "status_code": 200,  # Assume success unless error is set later
    }

    if isinstance(span_data, GenerationSpanData):
        data["input"] = span_data.input
        data["output"] = span_data.output
        data["model"] = span_data.model
        usage = _parse_usage(span_data.usage)
        data.update({f"num_{k}": v for k, v in usage.items() if v is not None})

        if span_data.model_config:
            # Ensure model_config is a dict
            model_config = span_data.model_config if isinstance(span_data.model_config, dict) else {}
            data["model_parameters"].update(model_config)
            data["temperature"] = model_config.get("temperature")
            data["metadata"]["model_config"] = model_config

    elif isinstance(span_data, ResponseSpanData):
        data["input"] = span_data.input
        if response := span_data.response:
            data["output"] = response.output
            data["model"] = response.model
            usage = _parse_usage(response.usage)
            data.update({f"num_{k}": v for k, v in usage.items() if v is not None})
            data["temperature"] = response.temperature

            # Extract tools
            tools_raw = getattr(response, "tools", None)
            if tools_raw:
                try:
                    data["tools"] = [t.model_dump() for t in tools_raw if hasattr(t, "model_dump")]
                except Exception:
                    _logger.debug("Failed to serialize tools.", exc_info=True)
                    data["tools"] = serialize_to_str(tools_raw)

            # Extract metadata and model parameters
            try:
                response_meta = response.model_dump(
                    exclude={"input", "output", "usage", "tools", "error", "status"}, exclude_none=True
                )
                data["metadata"]["response_metadata"] = response_meta
            except Exception:
                _logger.debug("Failed to model_dump response metadata.", exc_info=True)
                response_meta = {}  # Fallback

            data["model_parameters"] = {
                k: v
                for k, v in response_meta.items()
                if k
                in (
                    "temperature",
                    "max_output_tokens",
                    "top_p",
                    "tool_choice",
                    "parallel_tool_calls",
                    "truncation",
                    "seed",
                    "frequency_penalty",
                    "presence_penalty",
                )
            }
            # Add serialized tools to model parameters for context
            if data["tools"]:
                data["model_parameters"]["tools"] = data["tools"]

            # Handle potential error in response object
            if hasattr(response, "error") and response.error:
                data["metadata"]["error_details"] = response.error
                # Use 500 as default if status_code is not present on error
                data["status_code"] = getattr(response.error, "status_code", 500)

            # Include instructions in metadata if available
            if hasattr(response, "instructions") and response.instructions:
                data["metadata"]["instructions"] = response.instructions

    # Serialize complex inputs/outputs for logging
    # Galileo expects input/output as serialized strings for llm spans
    data["input"] = serialize_to_str(data["input"])
    data["output"] = serialize_to_str(data["output"])

    if data["temperature"] is not None:
        try:
            data["temperature"] = float(data["temperature"])
        except (ValueError, TypeError):
            data["temperature"] = None

    # Clean up None values that add_llm_span doesn't expect, but keep necessary keys
    data = {k: v for k, v in data.items() if v is not None or k in ["input", "output", "metadata", "model_parameters"]}

    return data


def _extract_tool_data(span_data: Union[FunctionSpanData, GuardrailSpanData]) -> dict[str, Any]:
    """Extract data specific to Tool spans (Function, Guardrail)."""
    data: dict[str, Any] = {
        "input": None,
        "output": None,
        "metadata": {},
        "status_code": 200,  # Assume success
    }
    if isinstance(span_data, FunctionSpanData):
        data["input"] = serialize_to_str(span_data.input)
        data["output"] = serialize_to_str(span_data.output)
    elif isinstance(span_data, GuardrailSpanData):
        data["input"] = None  # Guardrails might not map directly
        data["output"] = serialize_to_str({"triggered": span_data.triggered})
        data["metadata"]["triggered"] = span_data.triggered
        if span_data.triggered:
            # Indicate potential issue if guardrail triggered
            # Note: Galileo doesn't have a specific warning status, use metadata
            data["metadata"]["status"] = "warning"

    # Clean up None values, keeping essential keys
    data = {k: v for k, v in data.items() if v is not None or k in ["input", "output", "metadata"]}
    return data


def _extract_workflow_data(span_data: Union[AgentSpanData, HandoffSpanData, CustomSpanData]) -> dict[str, Any]:
    """Extract data specific to Workflow spans (Agent, Handoff, Custom)."""
    data: dict[str, Any] = {
        "input": None,
        "output": None,
        "metadata": {},
        "status_code": 200,  # Assume success
    }
    if isinstance(span_data, AgentSpanData):
        # Agent input/output is often implicit; capture config in metadata
        # We might get input/output later from children spans
        # Use getattr for safety in case these attributes aren't guaranteed
        data["metadata"]["tools"] = getattr(span_data, "tools", None)
        data["metadata"]["handoffs"] = getattr(span_data, "handoffs", None)
        data["metadata"]["output_type"] = getattr(span_data, "output_type", None)
    elif isinstance(span_data, HandoffSpanData):
        data["input"] = serialize_to_str({"from_agent": span_data.from_agent})
        data["output"] = serialize_to_str({"to_agent": span_data.to_agent})
        data["metadata"]["from_agent"] = span_data.from_agent
        data["metadata"]["to_agent"] = span_data.to_agent
    elif isinstance(span_data, CustomSpanData):
        custom_data_dict = span_data.data or {}
        data["input"] = serialize_to_str(custom_data_dict.get("input"))
        data["output"] = serialize_to_str(custom_data_dict.get("output"))
        # Filter out None values from metadata more carefully
        data["metadata"] = {k: v for k, v in custom_data_dict.items() if k not in ["input", "output"] and v is not None}

    # Clean up None values, keeping essential keys and non-empty metadata
    data = {k: v for k, v in data.items() if (v is not None and v != {}) or k in ["input", "output"]}
    # Ensure metadata is always a dict, even if empty after filtering
    if "metadata" not in data:
        data["metadata"] = {}

    return data
