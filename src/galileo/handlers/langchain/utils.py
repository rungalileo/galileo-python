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


def parse_llm_result(response: Any) -> LLMEndResult:
    """Extract serialized output and token metrics from a LangChain LLMResult.

    Handles three token-usage sources (checked in order):
    1. ``response.llm_output["token_usage"]`` with OpenAI keys (``prompt_tokens`` / ``completion_tokens``).
    2. Same dict with GCP Vertex AI keys (``input_tokens`` / ``output_tokens``).
    3. ``ChatGeneration.message.usage_metadata`` when ``llm_output`` carries no usage.

    Parameters
    ----------
    response
        A ``langchain_core.outputs.LLMResult`` (typed as ``Any`` to avoid import).
    """
    token_usage: dict[str, Any] = response.llm_output.get("token_usage", {}) if response.llm_output else {}

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

    return LLMEndResult(
        output=output,
        num_input_tokens=token_usage.get("prompt_tokens") or token_usage.get("input_tokens"),
        num_output_tokens=token_usage.get("completion_tokens") or token_usage.get("output_tokens"),
        total_tokens=token_usage.get("total_tokens"),
    )
