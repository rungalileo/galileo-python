from typing import Any, Literal, Optional
from uuid import UUID

SPAN_TYPE = Literal["llm", "retriever", "tool", "workflow"]
LANGCHAIN_NODE_TYPE = Literal["agent", "chain", "chat", "llm", "retriever", "tool"]


class Node:
    """
    A node in the Langchain trace.

    Attributes
    ----------
    node_type : LANGCHAIN_NODE_TYPE
        The type of node.
    span_params : dict[str, Any]
        The parameters for the span that will be created.
    run_id : UUID
        The run ID of the span.
    parent_run_id : Optional[UUID]
        The run ID of the parent span.
    children : List[str]
        List of run_ids for child nodes
    """

    def __init__(
        self,
        node_type: LANGCHAIN_NODE_TYPE,
        span_params: dict[str, Any],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        self.node_type: LANGCHAIN_NODE_TYPE = node_type
        self.span_params: dict[str, Any] = span_params
        self.run_id: UUID = run_id
        self.parent_run_id: Optional[UUID] = parent_run_id
        self.children: list[str] = []
