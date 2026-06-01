from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from galileo.schema.handlers import Node
from galileo.utils.serialization import EventSerializer
from galileo.utils.uuid_utils import convert_uuid_if_uuid7

_logger = logging.getLogger(__name__)


def get_agent_name(parent_run_id: UUID | None, node_name: str, nodes: dict[str, Node]) -> str:
    if parent_run_id is not None:
        # Convert UUID7 to UUID4 if needed
        parent_run_id = convert_uuid_if_uuid7(parent_run_id) or parent_run_id
        parent = nodes.get(str(parent_run_id))
        if parent:
            return parent.span_params["name"] + ":" + node_name
    return node_name


def is_agent_node(node_name: str) -> bool:
    return node_name.lower() in ["langgraph", "agent"]


def update_root_to_agent(parent_run_id: UUID | None, metadata: dict[str, Any], parent_node: Node | None) -> None:
    """Update the parent node to be an agent if it is a root-level chain and has LangGraph metadata in the children.

    Parameters
    ----------
    parent_run_id : Optional[UUID]
    metadata : dict[str, Any]
    parent_node : Optional[Node]
    """
    # Check if this node has LangGraph metadata - if so, its parent might be an agent
    # Only mark as agent if parent is a root-level chain (no grandparent)
    if parent_run_id and metadata and any(key.startswith("langgraph_") for key in metadata):
        # Only convert to agent if parent is a root-level chain (no parent of its own)
        if parent_node and parent_node.node_type == "chain" and parent_node.parent_run_id is None:
            parent_node.node_type = "agent"


@dataclass
class LLMEndResult:
    output: Any
    num_input_tokens: int | None
    num_output_tokens: int | None
    total_tokens: int | None
    image_input_tokens: int | None = None
    audio_input_tokens: int | None = None
    audio_output_tokens: int | None = None


def _extract_gemini_modality_breakdown(message: Any) -> tuple[int | None, int | None, int | None]:
    """Extract per-modality token counts from a LangChain AIMessage for Gemini native path.

    Returns (image_input_tokens, audio_input_tokens, audio_output_tokens).
    Returns (None, None, None) when no modality breakdown is available.

    Checks two surfaces:
    1. ``message.usage_metadata`` → ``input_token_details`` / ``output_token_details``
       (langchain-google-genai >= 2.x with LangChain Core UsageMetadata).
    2. ``message.response_metadata`` → ``prompt_tokens_details`` / ``candidates_tokens_details``
       (raw Gemini API token detail lists forwarded by the provider adapter).
    """
    image_in: int | None = None
    audio_in: int | None = None
    audio_out: int | None = None

    msg = getattr(message, "message", None)
    if msg is None:
        return None, None, None

    # Surface 1: usage_metadata.input_token_details / output_token_details
    usage_meta = getattr(msg, "usage_metadata", None)
    if isinstance(usage_meta, dict):
        input_details = usage_meta.get("input_token_details") or {}
        output_details = usage_meta.get("output_token_details") or {}
        if isinstance(input_details, dict):
            if "audio" in input_details:
                audio_in = input_details["audio"]
            if "image" in input_details:
                image_in = input_details["image"]
        if isinstance(output_details, dict):
            if "audio" in output_details:
                audio_out = output_details["audio"]

    # Surface 2: response_metadata prompt_tokens_details / candidates_tokens_details
    # (list of dicts like {"modality": "AUDIO", "token_count": N})
    response_meta = getattr(msg, "response_metadata", None)
    if isinstance(response_meta, dict):
        prompt_details = response_meta.get("prompt_tokens_details") or []
        candidates_details = response_meta.get("candidates_tokens_details") or []
        for entry in prompt_details:
            if not isinstance(entry, dict):
                continue
            modality = str(entry.get("modality", "")).upper()
            count = entry.get("token_count") or 0
            if modality == "AUDIO" and audio_in is None:
                audio_in = count
            elif modality == "IMAGE" and image_in is None:
                image_in = count
        for entry in candidates_details:
            if not isinstance(entry, dict):
                continue
            modality = str(entry.get("modality", "")).upper()
            count = entry.get("token_count") or 0
            if modality == "AUDIO" and audio_out is None:
                audio_out = count

    if image_in is None and audio_in is None and audio_out is None:
        return None, None, None
    return image_in, audio_in, audio_out


def parse_llm_result(response: Any) -> LLMEndResult:
    """Extract serialized output and token metrics from a LangChain LLMResult.

    Handles three token-usage sources (checked in order):
    1. ``response.llm_output["token_usage"]`` with OpenAI keys (``prompt_tokens`` / ``completion_tokens``).
    2. Same dict with GCP Vertex AI keys (``input_tokens`` / ``output_tokens``).
    3. ``ChatGeneration.message.usage_metadata`` when ``llm_output`` carries no usage.

    For Gemini native path (ChatGoogleGenerativeAI), also extracts per-modality token counts
    from ``message.usage_metadata.input_token_details`` and ``message.response_metadata``.

    Parameters
    ----------
    response
        A ``langchain_core.outputs.LLMResult`` (typed as ``Any`` to avoid import).
    """
    token_usage: dict[str, Any] = response.llm_output.get("token_usage", {}) if response.llm_output else {}

    first_message = None
    try:
        flattened_messages = [message for batch in response.generations for message in batch]
        first_message = flattened_messages[0] if flattened_messages else None
        if first_message is None:
            # Empty generations - fall back to stringified representation
            output = str(response.generations)
        else:
            output = json.loads(json.dumps(first_message, cls=EventSerializer))
            if not token_usage and hasattr(first_message, "message"):
                message_token_usage = getattr(getattr(first_message, "message", {}), "usage_metadata", None)
                if message_token_usage:
                    token_usage = {**token_usage, **message_token_usage}
    except Exception as e:
        _logger.warning(f"Failed to serialize LLM output: {e}")
        output = str(response.generations)

    image_in, audio_in, audio_out = (None, None, None)
    if first_message is not None:
        try:
            image_in, audio_in, audio_out = _extract_gemini_modality_breakdown(first_message)
        except Exception as e:
            _logger.debug(f"Failed to extract Gemini modality breakdown: {e}")

    return LLMEndResult(
        output=output,
        num_input_tokens=token_usage.get("prompt_tokens") or token_usage.get("input_tokens"),
        num_output_tokens=token_usage.get("completion_tokens") or token_usage.get("output_tokens"),
        total_tokens=token_usage.get("total_tokens"),
        image_input_tokens=image_in,
        audio_input_tokens=audio_in,
        audio_output_tokens=audio_out,
    )
