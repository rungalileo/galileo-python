from typing import Any, Optional
from uuid import UUID

from galileo.schema.handlers import Node
from galileo.utils.uuid_utils import convert_uuid_if_uuid7


def get_agent_name(parent_run_id: Optional[UUID], node_name: str, nodes: dict[str, Node]) -> str:
    if parent_run_id is not None:
        # Convert UUID7 to UUID4 if needed
        parent_run_id = convert_uuid_if_uuid7(parent_run_id) or parent_run_id
        parent = nodes.get(str(parent_run_id))
        if parent:
            return parent.span_params["name"] + ":" + node_name
    return node_name


def is_agent_node(node_name: str) -> bool:
    return node_name.lower() in ["langgraph", "agent"]


def update_root_to_agent(parent_run_id: Optional[UUID], metadata: dict[str, Any], parent_node: Optional[Node]) -> None:
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
