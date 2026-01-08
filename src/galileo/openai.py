"""
Galileo wrapper for OpenAI that automatically logs prompts and responses.

This module provides a drop-in replacement for the OpenAI library that automatically
logs all prompts, responses, and related metadata to Galileo. It works by intercepting
calls to the OpenAI API and logging them using the Galileo logging system.

Note that the original OpenAI package is still required as a project dependency to use this wrapper.

Examples
--------
```python
# Import the wrapped OpenAI client instead of the original
from galileo.openai import openai

# Use it exactly as you would use the regular OpenAI client
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me about the solar system."}
    ]
)

# All prompts and responses are automatically logged to Galileo
print(response.choices[0].message.content)

# You can also use it with the galileo_context for more control
from galileo import galileo_context

with galileo_context(project="my-project", log_stream="my-log-stream"):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me about the solar system."}
        ]
    )
```
"""

import json
import logging
import types
from collections import defaultdict
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from datetime import datetime
from inspect import isclass
from typing import Any, Callable, Optional, Union

import httpx
from pydantic import BaseModel
from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]

from galileo import GalileoLogger, Message, MessageRole, ToolCall, ToolCallFunction
from galileo.decorator import galileo_context
from galileo.utils import _get_timestamp
from galileo.utils.serialization import serialize_to_str

try:
    import openai
    from openai._types import NotGiven
    from openai.types import Reasoning
    from openai.types.chat import ChatCompletionMessageToolCall
    from openai.types.responses import (
        ResponseCodeInterpreterToolCall,
        ResponseComputerToolCall,
        ResponseFileSearchToolCall,
        ResponseFunctionToolCall,
        ResponseFunctionWebSearch,
        ResponseOutputMessage,
        ResponseReasoningItem,
    )
    from openai.types.responses.response_output_item import ImageGenerationCall, LocalShellCall, McpCall, McpListTools

    # it's used only for version check of OpenAI
    from packaging.version import Version
except ImportError:
    raise ModuleNotFoundError("Please install OpenAI to use this feature: 'pip install openai'")

try:
    from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI, NoneType, OpenAI  # noqa: F401
except ImportError:
    AsyncAzureOpenAI = None  # type: ignore[assignment]
    AsyncOpenAI = None  # type: ignore[assignment]
    AzureOpenAI = None  # type: ignore[assignment]
    OpenAI = None  # type: ignore[assignment]


@dataclass
class OpenAiModuleDefinition:
    module: str
    object: str
    method: str
    type: str
    sync: bool
    min_version: Optional[str] = None


@dataclass
class OpenAiInputData:
    name: str
    metadata: dict
    start_time: datetime
    input: str
    model_parameters: dict
    model: Optional[str]
    temperature: float
    tools: Optional[list[dict]]


_logger = logging.getLogger(__name__)


OPENAI_CLIENT_METHODS = [
    OpenAiModuleDefinition(
        module="openai.resources.chat.completions", object="Completions", method="create", type="chat", sync=True
    ),
    OpenAiModuleDefinition(
        module="openai.resources.responses", object="Responses", method="create", type="response", sync=True
    ),
    # Eventually add more OpenAI client library methods here
]


class OpenAiArgsExtractor:
    def __init__(self, name: Optional[str] = None, metadata: Optional[dict] = None, **kwargs: Any) -> None:
        self.args = {
            "name": name,
            "metadata": (
                metadata
                if "response_format" not in kwargs
                else {
                    **(metadata or {}),
                    "response_format": (
                        kwargs["response_format"].model_json_schema()
                        if isclass(kwargs["response_format"]) and issubclass(kwargs["response_format"], BaseModel)
                        else kwargs["response_format"]
                    ),
                }
            ),
        }
        self.kwargs = kwargs

    def get_galileo_args(self) -> dict[str, Any]:
        return {**self.args, **self.kwargs}

    def get_openai_args(self) -> dict[str, Any]:
        # If OpenAI model distillation is enabled, we need to add the metadata to the kwargs
        # https://platform.openai.com/docs/guides/distillation
        if self.kwargs.get("store", False):
            self.kwargs["metadata"] = self.args.get("metadata", {})

            # OpenAI does not support non-string type values in metadata when using
            # model distillation feature
            self.kwargs["metadata"].pop("response_format", None)

        return self.kwargs


def _galileo_wrapper(func: Callable) -> Callable:
    def _with_galileo(open_ai_definitions: OpenAiModuleDefinition, initialize: Callable) -> Callable:
        def wrapper(wrapped: Callable, instance: Any, args: dict, kwargs: dict) -> Any:
            return func(open_ai_definitions, initialize, wrapped, args, kwargs)

        return wrapper

    return _with_galileo


def _convert_to_galileo_message(data: Any, default_role: str = "user") -> Message:
    """Convert OpenAI response data to a Galileo Message object."""
    if hasattr(data, "type") and data.type == "function_call":
        tool_call = ToolCall(
            id=getattr(data, "call_id", ""),
            function=ToolCallFunction(name=getattr(data, "name", ""), arguments=getattr(data, "arguments", "")),
        )
        return Message(content="", role=MessageRole.assistant, tool_calls=[tool_call])

    if isinstance(data, dict) and data.get("type") == "function_call_output":
        output = data.get("output", "")
        content = json.dumps(output) if isinstance(output, dict) else str(output)

        return Message(content=content, role=MessageRole.tool, tool_call_id=data.get("call_id", ""))

    # Handle ChatCompletionMessage objects (from completion API) and dictionary messages
    if (hasattr(data, "role") and hasattr(data, "content")) or isinstance(data, dict):
        # Extract role and content from either object type
        if hasattr(data, "role"):
            # ChatCompletionMessage object
            role = getattr(data, "role", default_role)
            content = getattr(data, "content", "")
            tool_calls = getattr(data, "tool_calls", None)
            tool_call_id = getattr(data, "tool_call_id", None)
        else:
            # Dictionary message
            role = data.get("role", default_role)
            content = data.get("content", "")
            tool_calls = data.get("tool_calls")
            tool_call_id = data.get("tool_call_id")

        # Handle tool calls if present
        galileo_tool_calls = None
        if tool_calls:
            galileo_tool_calls = []
            for tc in tool_calls:
                if hasattr(tc, "function"):
                    # ChatCompletionMessageFunctionToolCall object
                    galileo_tool_calls.append(
                        ToolCall(
                            id=getattr(tc, "id", ""),
                            function=ToolCallFunction(
                                name=getattr(tc.function, "name", ""), arguments=getattr(tc.function, "arguments", "")
                            ),
                        )
                    )
                elif isinstance(tc, dict) and "function" in tc:
                    # Dictionary tool call
                    galileo_tool_calls.append(
                        ToolCall(
                            id=tc.get("id", ""),
                            function=ToolCallFunction(
                                name=tc["function"].get("name", ""), arguments=tc["function"].get("arguments", "")
                            ),
                        )
                    )

        return Message(
            content=str(content) if content is not None else "",
            role=MessageRole(role),
            tool_calls=galileo_tool_calls,
            tool_call_id=tool_call_id,
        )
    return Message(content=str(data), role=MessageRole(default_role))


def _extract_chat_response(kwargs: dict) -> dict:
    """Extracts the llm output from the response."""
    response = {"role": kwargs.get("role")}

    if kwargs.get("function_call") is not None and type(kwargs["function_call"]) is dict:
        response.update(
            {
                "tool_calls": [
                    {
                        "id": "",
                        "function": {
                            "name": kwargs["function_call"].get("name", ""),
                            "arguments": kwargs["function_call"].get("arguments", ""),
                        },
                    }
                ]
            }
        )
    elif kwargs.get("tool_calls") is not None and type(kwargs["tool_calls"]) is list:
        tool_calls = []
        for tool_call in kwargs["tool_calls"]:
            try:
                tool_call = ChatCompletionMessageToolCall.model_validate(tool_call)
                tool_calls.append(
                    {
                        "id": tool_call.id,
                        "function": {"name": tool_call.function.name, "arguments": tool_call.function.arguments},
                    }
                )
            except Exception as e:
                _logger.error(f"Error processing tool call: {e}")

        response.update({"tool_calls": tool_calls if tool_calls else None})

    response.update({"content": kwargs.get("content", "")})

    return response


def _extract_input_data_from_kwargs(
    resource: OpenAiModuleDefinition, start_time: datetime, kwargs: dict[str, Any]
) -> OpenAiInputData:
    name: str = kwargs.get("name", "openai-client-generation")

    if name is not None and not isinstance(name, str):
        raise TypeError("name must be a string")

    metadata: dict = kwargs.get("metadata", {})

    if metadata is not None and not isinstance(metadata, dict):
        raise TypeError("metadata must be a dictionary")

    model = kwargs.get("model") or None

    prompt = None

    if resource.type == "completion":
        prompt = kwargs.get("prompt")
    elif resource.type == "chat":
        prompt = kwargs.get("messages", [])
    elif resource.type == "response":
        prompt = kwargs.get("input", "")
        # TODO: parse instructions from kwargs
        # https://platform.openai.com/docs/guides/text#message-roles-and-instruction-following

    parsed_temperature = float(
        kwargs.get("temperature", 1) if not isinstance(kwargs.get("temperature", 1), NotGiven) else 1
    )

    parsed_max_tokens = (
        kwargs.get("max_tokens", float("inf"))
        if not isinstance(kwargs.get("max_tokens", float("inf")), NotGiven)
        else float("inf")
    )

    parsed_top_p = kwargs.get("top_p", 1) if not isinstance(kwargs.get("top_p", 1), NotGiven) else 1

    parsed_frequency_penalty = (
        kwargs.get("frequency_penalty", 0) if not isinstance(kwargs.get("frequency_penalty", 0), NotGiven) else 0
    )

    parsed_presence_penalty = (
        kwargs.get("presence_penalty", 0) if not isinstance(kwargs.get("presence_penalty", 0), NotGiven) else 0
    )

    parsed_seed = kwargs.get("seed") if not isinstance(kwargs.get("seed"), NotGiven) else None

    parsed_n = kwargs.get("n", 1) if not isinstance(kwargs.get("n", 1), NotGiven) else 1

    parsed_tools = kwargs.get("tools") if not isinstance(kwargs.get("tools"), NotGiven) else None

    parsed_tool_choice = kwargs.get("tool_choice") if not isinstance(kwargs.get("tool_choice"), NotGiven) else None

    # Extract reasoning parameters for Responses API
    reasoning: Optional[Union[Reasoning, dict]] = kwargs.get("reasoning") if resource.type == "response" else None
    if reasoning:
        # Handle both Reasoning object and dict types
        if isinstance(reasoning, Reasoning):
            parsed_reasoning_effort = reasoning.effort
            parsed_reasoning_verbosity = reasoning.summary
            parsed_reasoning_generate_summary = reasoning.generate_summary
        elif isinstance(reasoning, dict):
            parsed_reasoning_effort = reasoning.get("effort")
            parsed_reasoning_verbosity = reasoning.get("summary")
            parsed_reasoning_generate_summary = reasoning.get("generate_summary")
        else:
            parsed_reasoning_effort = getattr(reasoning, "effort", None)
            parsed_reasoning_verbosity = getattr(reasoning, "summary", None)
            parsed_reasoning_generate_summary = getattr(reasoning, "generate_summary", None)
    else:
        parsed_reasoning_effort = None
        parsed_reasoning_verbosity = None
        parsed_reasoning_generate_summary = None
    # handle deprecated aliases (functions for tools, function_call for tool_choice)
    if parsed_tools is None and kwargs.get("functions") is not None:
        parsed_tools = kwargs["functions"]

    if parsed_tool_choice is None and kwargs.get("function_call") is not None:
        parsed_tool_choice = kwargs["function_call"]

    model_parameters = {
        "temperature": parsed_temperature,
        "max_tokens": parsed_max_tokens,
        "top_p": parsed_top_p,
        "frequency_penalty": parsed_frequency_penalty,
        "presence_penalty": parsed_presence_penalty,
        "tool_choice": parsed_tool_choice,
    }
    if parsed_n is not None and parsed_n > 1:
        model_parameters["n"] = parsed_n

    if parsed_seed is not None:
        model_parameters["seed"] = parsed_seed

    # Add reasoning parameters to model parameters
    if parsed_reasoning_effort is not None:
        model_parameters["reasoning_effort"] = parsed_reasoning_effort
    if parsed_reasoning_verbosity is not None:
        model_parameters["reasoning_verbosity"] = parsed_reasoning_verbosity
    if parsed_reasoning_generate_summary is not None:
        model_parameters["reasoning_generate_summary"] = parsed_reasoning_generate_summary

    return OpenAiInputData(
        name=name,
        metadata=metadata,
        start_time=start_time,
        # TODO: galileo/openai.py:229: error:
        # Argument "input" to "OpenAiInputData" has incompatible type "Any | None"; expected "str"  [arg-type]
        input=prompt,  # type: ignore[arg-type]
        model_parameters=model_parameters,
        model=model or None,
        temperature=parsed_temperature,
        tools=parsed_tools,
    )


def _parse_usage(usage: Optional[dict] = None) -> Optional[dict]:
    if usage is None:
        return None

    usage_dict = usage.copy() if isinstance(usage, dict) else usage.__dict__

    # Handle Responses API field names (input_tokens/output_tokens) vs Chat Completions (prompt_tokens/completion_tokens)
    if "input_tokens" in usage_dict:
        usage_dict["input_tokens"] = usage_dict.pop("input_tokens")
    if "output_tokens" in usage_dict:
        usage_dict["output_tokens"] = usage_dict.pop("output_tokens")

    if "input_tokens_details" in usage_dict:
        usage_dict.update(usage_dict.pop("input_tokens_details"))
    if "output_tokens_details" in usage_dict:
        usage_dict.update(usage_dict.pop("output_tokens_details"))

    return usage_dict


def _extract_reasoning_content(item: ResponseReasoningItem) -> str:
    """Extract reasoning content from a reasoning item. Combines multiple summary items into a single string."""
    summary = item.summary or []
    if summary:
        reasoning_texts = []
        for summary_item in summary:
            if hasattr(summary_item, "text"):
                reasoning_texts.append(summary_item.text)
            elif isinstance(summary_item, dict) and "text" in summary_item:
                reasoning_texts.append(summary_item["text"])
        return "\n\n".join(reasoning_texts)
    return ""


def _extract_message_content(item: ResponseOutputMessage) -> str:
    """Extract message content from a message item."""
    content = item.content or []
    if isinstance(content, list):
        text_parts = []
        for content_item in content:
            if hasattr(content_item, "text"):
                text_parts.append(content_item.text)
            elif isinstance(content_item, dict) and "text" in content_item:
                text_parts.append(content_item["text"])
        return "".join(text_parts)
    return str(content) if content else ""


def _extract_web_search_tool_data(item: ResponseFunctionWebSearch) -> tuple[str, str]:
    """Extract input/output data from a web_search_call item."""
    tool_status = item.status or ""
    action = item.action
    if action:
        input_data: dict[str, Any] = {"type": getattr(action, "type", "")}
        if hasattr(action, "query"):
            input_data["query"] = getattr(action, "query", "")
        if hasattr(action, "url"):
            input_data["url"] = getattr(action, "url", "")
        if hasattr(action, "pattern"):
            input_data["pattern"] = getattr(action, "pattern", "")
        tool_input = json.dumps(input_data, indent=2)

        output_data: dict[str, Any] = {}
        if hasattr(action, "sources") and action.sources:
            sources = getattr(action, "sources", [])
            output_data["sources"] = [
                source.__dict__ if hasattr(source, "__dict__") else str(source) for source in sources
            ]
        if not output_data:
            output_data = {"status": tool_status}
        tool_output = json.dumps(output_data, indent=2)
    else:
        tool_input = json.dumps({}, indent=2)
        tool_output = f"Status: {tool_status}"
    return tool_input, tool_output


def _extract_mcp_call_tool_data(item: McpCall) -> tuple[str, str]:
    """Extract input/output data from an mcp_call item."""
    tool_input = json.dumps(
        {"name": item.name or "", "server_label": item.server_label or "", "arguments": item.arguments or ""}, indent=2
    )
    tool_output = json.dumps({"output": item.output or ""}, indent=2)
    return tool_input, tool_output


def _extract_mcp_list_tools_data(item: McpListTools) -> tuple[str, str]:
    """Extract input/output data from an mcp_list_tools item."""
    tool_input = item.server_label or ""
    tools = item.tools or []
    tool_output = json.dumps([tool.__dict__ if hasattr(tool, "__dict__") else tool for tool in tools], indent=2)
    return tool_input, tool_output


def _extract_file_search_tool_data(item: ResponseFileSearchToolCall) -> tuple[str, str]:
    """Extract input/output data from a file_search_call item."""
    tool_status = item.status or ""
    tool_input = json.dumps(
        {
            "queries": item.queries or [],
            "results": [result.__dict__ if hasattr(result, "__dict__") else result for result in (item.results or [])],
        },
        indent=2,
    )
    tool_output = f"Status: {tool_status}"
    return tool_input, tool_output


def _extract_computer_call_tool_data(item: ResponseComputerToolCall) -> tuple[str, str]:
    """Extract input/output data from a computer_call item."""
    tool_status = item.status or ""
    action = item.action
    tool_input = json.dumps(action.__dict__ if action else {}, indent=2)
    tool_output = f"Status: {tool_status}"
    return tool_input, tool_output


def _extract_image_generation_tool_data(item: ImageGenerationCall) -> tuple[str, str]:
    """Extract input/output data from an image_generation_call item."""
    tool_input = json.dumps({"id": item.id or "", "status": item.status or ""}, indent=2)
    tool_output = item.result or ""
    return tool_input, tool_output


def _extract_code_interpreter_tool_data(item: ResponseCodeInterpreterToolCall) -> tuple[str, str]:
    """Extract input/output data from a code_interpreter_call item."""
    tool_input = json.dumps(
        {
            "id": item.id or "",
            "code": item.code or "",
            "container_id": item.container_id or "",
            "status": item.status or "",
        },
        indent=2,
    )
    outputs = item.outputs or []
    tool_output = json.dumps([o.__dict__ if hasattr(o, "__dict__") else o for o in outputs], indent=2)
    return tool_input, tool_output


def _extract_local_shell_tool_data(item: LocalShellCall) -> tuple[str, str]:
    """Extract input/output data from a local_shell_call item."""
    tool_status = item.status or ""
    action = item.action
    tool_input = json.dumps(
        {
            "id": item.id or "",
            "call_id": item.call_id or "",
            "status": item.status or "",
            "action": action.__dict__ if action else {},
        },
        indent=2,
    )
    tool_output = f"Status: {tool_status}"
    return tool_input, tool_output


def _extract_custom_tool_data(item: ResponseFunctionToolCall) -> tuple[str, str]:
    """Extract input/output data from a custom_tool_call (function tool call) item."""
    tool_status = item.status or ""
    tool_input = json.dumps({"name": item.name or "", "arguments": item.arguments or ""}, indent=2)
    tool_output = f"Status: {tool_status}"
    return tool_input, tool_output


def _extract_function_call_data(item: Any) -> tuple[str, str]:
    """Extract input/output data from a function_call item (model requesting to call a function)."""
    tool_input = json.dumps(
        {
            "name": getattr(item, "name", ""),
            "arguments": getattr(item, "arguments", ""),
            "call_id": getattr(item, "call_id", "") or getattr(item, "id", ""),
        },
        indent=2,
    )
    tool_output = json.dumps({"status": getattr(item, "status", "pending")}, indent=2)
    return tool_input, tool_output


def _extract_generic_tool_data(item: Any) -> tuple[str, str]:
    """Extract input/output data from an unknown tool type."""
    tool_status = getattr(item, "status", "")
    tool_input = json.dumps({"name": getattr(item, "name", ""), "arguments": getattr(item, "arguments", "")}, indent=2)
    tool_output = f"Status: {tool_status}\nOutput: {getattr(item, 'output', '')}"
    return tool_input, tool_output


# Mapping of tool types to their extraction functions
_TOOL_EXTRACTORS: dict[str, Callable[[Any], tuple[str, str]]] = {
    "web_search_call": _extract_web_search_tool_data,
    "mcp_call": _extract_mcp_call_tool_data,
    "mcp_list_tools": _extract_mcp_list_tools_data,
    "file_search_call": _extract_file_search_tool_data,
    "computer_call": _extract_computer_call_tool_data,
    "image_generation_call": _extract_image_generation_tool_data,
    "code_interpreter_call": _extract_code_interpreter_tool_data,
    "local_shell_call": _extract_local_shell_tool_data,
    "custom_tool_call": _extract_custom_tool_data,
    # Note: "function_call" is handled separately - it's joined with function_call_output
    # in _process_function_call_outputs to create a single combined tool span
}

# Tool call types that should create separate tool spans
# function_call is excluded because it's combined with function_call_output
TOOL_SPAN_TYPES = frozenset(_TOOL_EXTRACTORS.keys())


def _process_function_call_outputs(input_items: list, galileo_logger: GalileoLogger) -> None:
    """
    Process function_call and function_call_output items from the input and create combined tool spans.
    This joins the function call (model's request to call a tool) with the function output (tool result)
    into a single tool span, representing the complete tool execution.
    """
    # First, collect all function_call items by call_id (handle both object and dict forms)
    function_calls: dict[str, dict] = {}
    for item in input_items:
        # Check for object form (from SDK response objects)
        if hasattr(item, "type") and item.type == "function_call":
            call_id = getattr(item, "call_id", "") or getattr(item, "id", "")
            function_calls[call_id] = {
                "name": getattr(item, "name", ""),
                "arguments": getattr(item, "arguments", ""),
                "call_id": call_id,
            }
        # Check for dict form (when passed as dict in input)
        elif isinstance(item, dict) and item.get("type") == "function_call":
            call_id = item.get("call_id", "") or item.get("id", "")
            function_calls[call_id] = {
                "name": item.get("name", ""),
                "arguments": item.get("arguments", ""),
                "call_id": call_id,
            }

    # Then, process function_call_output items and match with function_calls
    for item in input_items:
        if isinstance(item, dict) and item.get("type") == "function_call_output":
            call_id = item.get("call_id", "")
            output = item.get("output", "")

            # Get matching function_call if available
            function_call = function_calls.get(call_id, {})

            # Create tool span with function call info as input and result as output
            tool_input = json.dumps(
                {
                    "name": function_call.get("name", ""),
                    "arguments": function_call.get("arguments", ""),
                    "call_id": call_id,
                },
                indent=2,
            )
            tool_output = json.dumps(output) if isinstance(output, dict) else str(output)

            galileo_logger.add_tool_span(
                input=tool_input,
                output=tool_output,
                name=function_call.get("name") or "function_call",
                metadata={"tool_id": call_id, "tool_type": "function_call"},
            )


def _process_output_items(
    output_items: list,
    galileo_logger: GalileoLogger,
    model: Optional[str] = None,
    original_input: Optional[list] = None,
    model_parameters: Optional[dict] = None,
    status_code: int = 200,
    tools: Optional[list] = None,
    usage: Optional[dict] = None,
) -> list:
    """
    The responses API returns an array of output items. This function processes output items sequentially,
    consolidating reasoning into the main response content and creating tool spans for specific tool call types.
    """
    conversation_context = original_input.copy() if original_input else []

    # Collect all reasoning content to include in the final response
    all_reasoning_content = []
    final_message_content = ""
    final_tool_calls = []

    # loop through output items to construct tool calls, messages, and reasoning
    for item in output_items:
        if hasattr(item, "type") and item.type == "reasoning":
            # Extract reasoning content but don't create separate spans
            reasoning_content = _extract_reasoning_content(item)
            if reasoning_content:
                all_reasoning_content.append(reasoning_content)

        elif hasattr(item, "type") and item.type == "message":
            # Extract message content
            message_content = _extract_message_content(item)
            final_message_content = message_content

        elif hasattr(item, "type") and item.type == "function_call":
            # Collect regular function calls (not tool spans)
            tool_call = {
                "id": getattr(item, "id", ""),
                "function": {"name": getattr(item, "name", ""), "arguments": getattr(item, "arguments", "")},
                "type": "function",
            }
            final_tool_calls.append(tool_call)

    # Create consolidated output with reasoning as separate Messages
    consolidated_output_messages = []

    # Add reasoning as special reasoning objects (not Message objects)
    if all_reasoning_content:
        for _i, reasoning_text in enumerate(all_reasoning_content):
            # Create a special reasoning object instead of a Message
            reasoning_obj = {"type": "reasoning", "content": reasoning_text}
            consolidated_output_messages.append(reasoning_obj)

    # Add the final response message
    if final_message_content:
        response_message = _convert_to_galileo_message(final_message_content, "assistant")
        consolidated_output_messages.append(response_message)

    # Create the final consolidated output for the LLM span with content and reasoning
    if consolidated_output_messages or final_tool_calls:
        # If there's no reasoning content, use the message content directly
        # Otherwise, serialize the array of Messages and reasoning objects into a string
        if not all_reasoning_content and final_message_content:
            # Simple case: just a message with no reasoning
            consolidated_output = _convert_to_galileo_message(final_message_content, "assistant")
        else:
            # Complex case: serialize the array of Messages and reasoning objects
            # WORKAROUND: Serialize into a string since LLM span output
            # doesn't support list of Messages. This is a temporary solution until better responses support is added.
            serialized_items = []
            for item in consolidated_output_messages:
                if isinstance(item, dict) and item.get("type") == "reasoning":
                    # Keep reasoning objects as-is
                    serialized_items.append(item)
                elif isinstance(item, Message):
                    serialized_items.append(item.model_dump(exclude_none=True))
                else:
                    # Convert to JSON string as fallback
                    serialized_items.append(json.dumps(item))

            messages_serialized = json.dumps(serialized_items, indent=2)

            # Create a single Message with the serialized array as content
            consolidated_output = _convert_to_galileo_message(messages_serialized, "assistant")

        # Add tool calls if present
        if final_tool_calls:
            consolidated_output.tool_calls = [
                ToolCall(
                    id=tc["id"],
                    function=ToolCallFunction(name=tc["function"]["name"], arguments=tc["function"]["arguments"]),
                )
                for tc in final_tool_calls
            ]

        # Create single consolidated span with serialized messages
        span = galileo_logger.add_llm_span(
            input=conversation_context,
            output=consolidated_output,
            model=model,
            name="response",
            tools=tools,
            status_code=status_code,
            num_input_tokens=usage.get("input_tokens", 0) if usage else 0,
            num_output_tokens=usage.get("output_tokens", 0) if usage else 0,
            total_tokens=usage.get("total_tokens", 0) if usage else 0,
            metadata={
                "type": "consolidated_response",
                "includes_reasoning": str(bool(all_reasoning_content)),
                "reasoning_count": str(len(all_reasoning_content)),
                "serialized_messages": "true",  # Flag to indicate this contains serialized messages
                **{str(k): str(v) for k, v in (model_parameters or {}).items()},
            },
        )
        span.metrics.num_reasoning_tokens = usage.get("reasoning_tokens", 0) if usage else 0
        span.metrics.num_cached_input_tokens = usage.get("cached_tokens", 0) if usage else 0

        # Update conversation context with only Message objects (not reasoning objects)
        for item in consolidated_output_messages:
            if not (isinstance(item, dict) and item.get("type") == "reasoning"):
                conversation_context.append(item)

    for item in output_items:
        if hasattr(item, "type") and item.type in TOOL_SPAN_TYPES:
            tool_id = getattr(item, "id", "")
            tool_status = getattr(item, "status", "")

            # Use the appropriate extractor function for this tool type
            extractor = _TOOL_EXTRACTORS.get(item.type, _extract_generic_tool_data)
            tool_input, tool_output = extractor(item)

            # Create tool span with the tool type as the name
            galileo_logger.add_tool_span(
                input=tool_input,
                output=tool_output,
                name=item.type,
                metadata={
                    "tool_id": tool_id,
                    "tool_type": item.type,
                    "tool_status": tool_status,
                    **{str(k): str(v) for k, v in (model_parameters or {}).items()},
                },
            )

    return conversation_context


def _extract_responses_output(output_items: list) -> dict:
    """Extract the final message and tool calls from Responses API output items."""
    final_message = None
    tool_calls = []

    for item in output_items:
        if hasattr(item, "type") and item.type == "message":
            final_message = {"role": getattr(item, "role", "assistant"), "content": ""}

            content = getattr(item, "content", [])
            if isinstance(content, list):
                text_parts = []
                for content_item in content:
                    if hasattr(content_item, "text"):
                        text_parts.append(content_item.text)
                    elif isinstance(content_item, dict) and "text" in content_item:
                        text_parts.append(content_item["text"])
                final_message["content"] = "".join(text_parts)
            else:
                final_message["content"] = str(content)

        elif hasattr(item, "type") and item.type == "function_call":
            tool_call = {
                "id": getattr(item, "id", ""),
                "function": {"name": getattr(item, "name", ""), "arguments": getattr(item, "arguments", "")},
                "type": "function",
            }
            tool_calls.append(tool_call)

    if final_message:
        if tool_calls:
            final_message["tool_calls"] = tool_calls
        return final_message
    if tool_calls:
        return {"role": "assistant", "tool_calls": tool_calls}
    return {"role": "assistant", "content": ""}


def _has_pending_function_calls(output_items: list) -> bool:
    """
    Check if the response has pending function calls that require tool execution.
    Returns True if there are function_call items but no final message content.
    This indicates the model is waiting for tool results before producing a final response.
    """
    has_function_call = False
    has_final_message = False

    for item in output_items:
        if hasattr(item, "type"):
            if item.type == "function_call":
                has_function_call = True
            elif item.type == "message":
                # Check if there's actual content in the message
                content = getattr(item, "content", [])
                if isinstance(content, list) and content:
                    for content_item in content:
                        if (hasattr(content_item, "text") and content_item.text) or (
                            isinstance(content_item, dict) and content_item.get("text")
                        ):
                            has_final_message = True
                            break
                elif content:
                    has_final_message = True

    # Pending function calls = has function_call but no final message
    return has_function_call and not has_final_message


def _extract_data_from_default_response(resource: OpenAiModuleDefinition, response: Optional[dict[str, Any]]) -> Any:
    if response is None:
        return None, "<NoneType response returned from OpenAI>", None

    model = response.get("model", None)

    completion = None
    if resource.type == "completion":
        choices = response.get("choices", [])
        if len(choices) > 0:
            choice = choices[-1]

            completion = choice.text if _is_openai_v1() else choice.get("text", None)
    elif resource.type == "chat":
        choices = response.get("choices", [])
        if len(choices):
            if len(choices) > 1:
                completion = [
                    (
                        _extract_chat_response(choice.message.__dict__)
                        if _is_openai_v1()
                        else choice.get("message", None)
                    )
                    for choice in choices
                ]
            else:
                choice = choices[0]
                completion = (
                    _extract_chat_response(choice.message.__dict__) if _is_openai_v1() else choice.get("message", None)
                )
    elif resource.type == "response":
        # Handle Responses API structure
        output = response.get("output", [])
        completion = _extract_responses_output(output)

    usage = _parse_usage(response.get("usage"))

    return model, completion, usage


def _extract_streamed_openai_response(resource: OpenAiModuleDefinition, chunks: Iterable) -> Any:
    completion: Any = defaultdict(lambda: None) if resource.type == "chat" else ""
    model, usage = None, None

    # For Responses API, we just need to find the final completed event
    if resource.type == "response":
        final_response = None

    for chunk in chunks:
        if _is_openai_v1():
            chunk = chunk.__dict__

        if resource.type == "response":
            chunk_type = chunk.get("type", "")

            if chunk_type == "response.completed":
                final_response = chunk.get("response")
                if final_response:
                    model = getattr(final_response, "model", None)
                    usage_obj = getattr(final_response, "usage", None)
                    if usage_obj:
                        usage = _parse_usage(usage_obj.__dict__ if hasattr(usage_obj, "__dict__") else usage_obj)

            continue

        model = model or chunk.get("model", None) or None
        usage = chunk.get("usage", None)

        choices = chunk.get("choices", [])

        for choice in choices:
            if _is_openai_v1():
                choice = choice.__dict__
            if resource.type == "chat":
                delta = choice.get("delta", None)

                if _is_openai_v1():
                    delta = delta.__dict__

                if delta.get("role", None) is not None:
                    completion["role"] = delta["role"]

                if delta.get("content", None) is not None:
                    completion["content"] = (
                        delta.get("content", None)
                        if completion["content"] is None
                        else completion["content"] + delta.get("content", None)
                    )
                elif delta.get("function_call", None) is not None:
                    curr = completion["function_call"]
                    tool_call_chunk = delta.get("function_call", None)

                    if not curr:
                        completion["function_call"] = {
                            "name": getattr(tool_call_chunk, "name", ""),
                            "arguments": getattr(tool_call_chunk, "arguments", ""),
                        }

                    else:
                        curr["name"] = curr["name"] or getattr(tool_call_chunk, "name", None)
                        curr["arguments"] += getattr(tool_call_chunk, "arguments", "")

                elif delta.get("tool_calls", None) is not None:
                    curr = completion["tool_calls"]
                    tool_call_chunk = getattr(delta.get("tool_calls", None)[0], "function", None)

                    if not curr:
                        completion["tool_calls"] = [
                            {
                                "name": getattr(tool_call_chunk, "name", ""),
                                "arguments": getattr(tool_call_chunk, "arguments", ""),
                            }
                        ]

                    elif getattr(tool_call_chunk, "name", None) is not None:
                        curr.append(
                            {
                                "name": getattr(tool_call_chunk, "name", None),
                                "arguments": getattr(tool_call_chunk, "arguments", None),
                            }
                        )

                    else:
                        curr[-1]["name"] = curr[-1]["name"] or getattr(tool_call_chunk, "name", None)
                        curr[-1]["arguments"] += getattr(tool_call_chunk, "arguments", None)

            if resource.type == "completion":
                completion += choice.get("text", None)

    def get_response_for_chat(completion: dict) -> Any:
        return (
            completion["content"]
            or (completion["function_call"] and {"role": "assistant", "function_call": completion["function_call"]})
            or (
                completion["tool_calls"]
                and {"role": "assistant", "tool_calls": [{"function": data} for data in completion["tool_calls"]]}
            )
            or None
        )

    if resource.type == "chat":
        return model, get_response_for_chat(completion), usage
    if resource.type == "response":
        if final_response:
            output_items = getattr(final_response, "output", [])
            # Since we get a response object back, we can use the same function to extract the output
            response_message = _extract_responses_output(output_items)
            # Return the full response structure so streaming can access output_items
            full_response = {
                "role": "assistant",
                "content": response_message.get("content", ""),
                "tool_calls": response_message.get("tool_calls"),
                "output": output_items,  # Include output items for processing
            }
            return model, full_response, usage
        return model, {"role": "assistant", "content": ""}, usage
    return model, completion, usage


def _is_openai_v1() -> bool:
    return Version(openai.__version__) >= Version("1.0.0")


def _is_streaming_response(response: Any) -> bool:
    return isinstance(response, types.GeneratorType) or (_is_openai_v1() and isinstance(response, openai.Stream))


@_galileo_wrapper
def _wrap(
    open_ai_resource: OpenAiModuleDefinition, initialize: Callable, wrapped: Callable, args: dict, kwargs: dict
) -> Any:
    start_time = _get_timestamp()
    arg_extractor = OpenAiArgsExtractor(*args, **kwargs)

    input_data = _extract_input_data_from_kwargs(open_ai_resource, start_time, arg_extractor.get_galileo_args())

    galileo_logger: GalileoLogger = initialize()

    should_complete_trace = False
    if galileo_logger.current_parent():
        pass
    else:
        # If we don't have an active trace, start a new trace
        # We will conclude it at the end
        # convert to list of galileo messages since we can't send list of messages to span and want consistency
        if isinstance(input_data.input, list):
            trace_input_messages = [_convert_to_galileo_message(msg) for msg in input_data.input]
        else:
            trace_input_messages = [_convert_to_galileo_message(input_data.input)]

        # Serialize with "messages" wrapper for UI compatibility
        trace_input = {"messages": [msg.model_dump(exclude_none=True) for msg in trace_input_messages]}
        galileo_logger.start_trace(input=serialize_to_str(trace_input), name=input_data.name)
        should_complete_trace = True

    try:
        openai_response = None
        exc_info = None
        status_code = httpx.codes.OK
        try:
            openai_response = wrapped(**arg_extractor.get_openai_args())
        except openai.APIStatusError as exc:
            status_code = exc.status_code
            exc_info = exc

        if _is_streaming_response(openai_response):
            # extract data from streaming response
            return ResponseGeneratorSync(
                resource=open_ai_resource,
                response=openai_response,
                input_data=input_data,
                logger=galileo_logger,
                should_complete_trace=should_complete_trace,
                status_code=status_code,
            )
        model, completion, usage = _extract_data_from_default_response(
            open_ai_resource, (openai_response.__dict__ if openai_response and _is_openai_v1() else openai_response)
        )

        if usage is None:
            usage = {}

        end_time = _get_timestamp()

        duration_ns = round((end_time - start_time).total_seconds() * 1e9)

        # convert to list of galileo messages since we can't send a regular list to span input
        if isinstance(input_data.input, list):
            span_input = [_convert_to_galileo_message(msg) for msg in input_data.input]
        else:
            span_input = [_convert_to_galileo_message(input_data.input)]

        # Process Responses API output items sequentially if present
        final_conversation_context = span_input.copy()
        output_items: list = []
        if open_ai_resource.type == "response" and openai_response:
            # First, process any function_call_output items in the input to create tool spans
            # This represents tool executions that happened before this API call
            if isinstance(input_data.input, list):
                _process_function_call_outputs(input_data.input, galileo_logger)

            response_dict = openai_response.__dict__ if _is_openai_v1() else openai_response
            output_items = response_dict.get("output", [])

            # Process all output items sequentially and get the final context
            final_conversation_context = _process_output_items(
                output_items,
                galileo_logger,
                model,
                span_input,
                input_data.model_parameters,
                status_code=status_code,
                tools=input_data.tools,
                usage=usage,
            )
        else:
            # For non-Responses API (chat or completion), create the main span as before
            span_output = _convert_to_galileo_message(completion, "assistant")

            # Add a span to the current trace or span (if this is a nested trace)
            span = galileo_logger.add_llm_span(
                input=span_input,
                output=span_output,
                tools=input_data.tools,
                name=input_data.name,
                model=model,
                temperature=input_data.temperature,
                duration_ns=duration_ns,
                num_input_tokens=usage.get("input_tokens", 0),
                num_output_tokens=usage.get("output_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                metadata={str(k): str(v) for k, v in input_data.model_parameters.items()},
                # openai client library doesn't return http_status code, so we only can hardcode it here
                # because we if we parsed and extracted data from response it means we get it and it's 200OK
                status_code=status_code,
            )
            span.metrics.num_reasoning_tokens = usage.get("reasoning_tokens", 0) if usage else 0
            span.metrics.num_cached_input_tokens = usage.get("cached_tokens", 0) if usage else 0

        # Conclude the trace if this is the top-level call
        # For Responses API: don't conclude if there are pending function calls (model waiting for tool results)
        has_pending_calls = (
            open_ai_resource.type == "response" and output_items and _has_pending_function_calls(output_items)
        )

        if should_complete_trace and not has_pending_calls:
            if open_ai_resource.type == "response":
                # For Responses API, use the final conversation context from processing
                full_conversation = final_conversation_context
            else:
                # For other APIs, add the final span output
                full_conversation = []
                if isinstance(input_data.input, list):
                    full_conversation.extend([_convert_to_galileo_message(msg) for msg in input_data.input])
                else:
                    full_conversation.append(_convert_to_galileo_message(input_data.input))
                full_conversation.append(span_output)

            # Serialize with "messages" wrapper for UI compatibility
            trace_output = {"messages": [msg.model_dump(exclude_none=True) for msg in full_conversation]}
            galileo_logger.conclude(
                output=serialize_to_str(trace_output), duration_ns=duration_ns, status_code=status_code
            )

        # we want to re-raise exception after we process openai_response
        if exc_info:
            raise exc_info
        return openai_response
    except Exception as ex:
        _logger.error(f"Error while processing OpenAI request: {ex}")
        raise RuntimeError("Failed to process the OpenAI Request") from ex


class ResponseGeneratorSync:
    """
    A wrapper for OpenAI streaming responses that logs the response to Galileo.

    This class wraps the OpenAI streaming response generator and logs the response
    to Galileo when the generator is exhausted. It implements the iterator protocol
    to allow for streaming responses.

    Attributes
    ----------
    resource : OpenAiModuleDefinition
        The OpenAI resource definition.
    response : Generator or openai.Stream
        The OpenAI streaming response.
    input_data : OpenAiInputData
        The input data for the OpenAI request.
    logger : GalileoLogger
        The Galileo logger instance.
    should_complete_trace : bool
        Whether to complete the trace when the generator is exhausted.
    """

    def __init__(
        self,
        *,
        resource: OpenAiModuleDefinition,
        response: Union[Generator, openai.Stream],
        input_data: OpenAiInputData,
        logger: GalileoLogger,
        should_complete_trace: bool,
        status_code: int = 200,
    ):
        self.items: list[Any] = []
        self.resource = resource
        self.response = response
        self.input_data = input_data
        self.logger = logger
        self.should_complete_trace = should_complete_trace
        self.completion_start_time: Optional[datetime] = None
        self.status_code = status_code

    def __iter__(self):
        try:
            for i in self.response:
                self.items.append(i)

                if self.completion_start_time is None:
                    self.completion_start_time = _get_timestamp()

                yield i
        finally:
            self._finalize()

    def __next__(self):
        try:
            item = self.response.__next__()
            self.items.append(item)

            if self.completion_start_time is None:
                self.completion_start_time = _get_timestamp()

            return item

        except StopIteration:
            self._finalize()

            raise

    def __enter__(self):
        return self.__iter__()

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        pass

    def _finalize(self) -> None:
        model, completion, usage = _extract_streamed_openai_response(self.resource, self.items)

        if usage is None:
            usage = {}

        end_time = _get_timestamp()
        # TODO: make sure completion_start_time what we want
        duration_ns = (
            round((end_time - self.completion_start_time).total_seconds() * 1e9) if self.completion_start_time else 0
        )

        if isinstance(self.input_data.input, list):
            span_input = [_convert_to_galileo_message(msg) for msg in self.input_data.input]
        else:
            span_input = [_convert_to_galileo_message(self.input_data.input)]

        # probably can create a shared function for handling both streaming and non-streaming
        # Process Responses API output items sequentially if present (same as non-streaming)
        final_conversation_context = span_input.copy()
        output_items: list = []
        if self.resource.type == "response" and completion:
            # First, process any function_call_output items in the input to create tool spans
            # This represents tool executions that happened before this API call
            if isinstance(self.input_data.input, list):
                _process_function_call_outputs(self.input_data.input, self.logger)

            # For streaming Responses API, we need to extract output items from the completion
            # The completion should contain the final response with output items
            if isinstance(completion, dict) and "output" in completion:
                output_items = completion.get("output", [])

                # Process all output items sequentially and get the final context
                final_conversation_context = _process_output_items(
                    output_items,
                    self.logger,
                    model,
                    span_input,
                    self.input_data.model_parameters,
                    status_code=self.status_code,
                    tools=self.input_data.tools,
                    usage=usage,
                )
            else:
                # Fallback: create basic span if no output items
                span_output = _convert_to_galileo_message(completion, "assistant")
                span = self.logger.add_llm_span(
                    input=span_input,
                    output=span_output,
                    tools=self.input_data.tools,
                    name=self.input_data.name,
                    model=model,
                    temperature=self.input_data.temperature,
                    duration_ns=duration_ns,
                    num_input_tokens=usage.get("input_tokens", 0),
                    num_output_tokens=usage.get("output_tokens", 0),
                    total_tokens=usage.get("total_tokens", 0),
                    metadata={str(k): str(v) for k, v in self.input_data.model_parameters.items()},
                    status_code=self.status_code,
                )
                span.metrics.num_reasoning_tokens = usage.get("reasoning_tokens", 0) if usage else 0
                span.metrics.num_cached_input_tokens = usage.get("cached_tokens", 0) if usage else 0
        else:
            # For non-Responses API (chat or completion), create the main span as before
            span_output = _convert_to_galileo_message(completion, "assistant")

            # Add a span to the current trace or span (if this is a nested trace)
            span = self.logger.add_llm_span(
                input=span_input,
                output=span_output,
                tools=self.input_data.tools,
                name=self.input_data.name,
                model=model,
                temperature=self.input_data.temperature,
                duration_ns=duration_ns,
                num_input_tokens=usage.get("input_tokens", 0),
                num_output_tokens=usage.get("output_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                metadata={str(k): str(v) for k, v in self.input_data.model_parameters.items()},
                status_code=self.status_code,
            )
            span.metrics.num_reasoning_tokens = usage.get("reasoning_tokens", 0) if usage else 0
            span.metrics.num_cached_input_tokens = usage.get("cached_tokens", 0) if usage else 0

        # Conclude the trace if this is the top-level call
        # For Responses API: don't conclude if there are pending function calls (model waiting for tool results)
        has_pending_calls = (
            self.resource.type == "response" and output_items and _has_pending_function_calls(output_items)
        )

        if self.should_complete_trace and not has_pending_calls:
            if self.resource.type == "response":
                # For Responses API, use the final conversation context from processing
                full_conversation = final_conversation_context
            else:
                # For other APIs, add the final span output
                full_conversation = []
                if isinstance(self.input_data.input, list):
                    full_conversation.extend([_convert_to_galileo_message(msg) for msg in self.input_data.input])
                else:
                    full_conversation.append(_convert_to_galileo_message(self.input_data.input))
                full_conversation.append(_convert_to_galileo_message(completion, "assistant"))

            # Serialize with "messages" wrapper for UI compatibility
            trace_output = {"messages": [msg.model_dump(exclude_none=True) for msg in full_conversation]}
            self.logger.conclude(
                output=serialize_to_str(trace_output), duration_ns=duration_ns, status_code=self.status_code
            )


class OpenAIGalileo:
    """
    This class is responsible for logging OpenAI API calls and logging them to Galileo.
    It wraps the OpenAI client methods to add logging functionality without changing
    the original API behavior.

    Attributes
    ----------
    _galileo_logger : Optional[GalileoLogger]
        The Galileo logger instance used for logging OpenAI API calls.
    """

    _galileo_logger: Optional[GalileoLogger] = None

    def initialize(self) -> Optional[GalileoLogger]:
        """
        Initialize a Galileo logger.

        Parameters
        ----------
        project : Optional[str]
            The project to log to. If None, uses the default project.
        log_stream : Optional[str]
            The log stream to log to. If None, uses the default log stream.

        Returns
        -------
        Optional[GalileoLogger]
            The initialized Galileo logger instance.
        """
        self._galileo_logger = galileo_context.get_logger_instance()

        return self._galileo_logger

    def register_tracing(self) -> None:
        """
        This method wraps the OpenAI client methods to intercept calls and log them to Galileo.
        It is called automatically when the module is imported.

        The wrapped methods include:
        - openai.resources.chat.completions.Completions.create

        Additional methods can be added to the OPENAI_CLIENT_METHODS list.
        """
        for resource in OPENAI_CLIENT_METHODS:
            wrap_function_wrapper(
                resource.module, f"{resource.object}.{resource.method}", (_wrap(resource, self.initialize))
            )


modifier = OpenAIGalileo()
modifier.register_tracing()
