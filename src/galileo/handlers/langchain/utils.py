from typing import Optional
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
