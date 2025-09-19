from typing import Optional
from uuid import UUID

from galileo.schema.handlers import Node


def get_agent_name(parent_run_id: Optional[UUID], node_name: str, nodes: dict[str, Node]) -> str:
    if parent_run_id is not None:
        parent = nodes.get(str(parent_run_id))
        if parent:
            return parent.span_params["name"] + ":" + node_name
    return node_name


def is_agent_node(node_name: str) -> bool:
    return node_name in ["LangGraph", "Agent"]
