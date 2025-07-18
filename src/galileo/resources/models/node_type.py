from typing import Literal, cast

NodeType = Literal["agent", "chain", "chat", "llm", "retriever", "session", "tool", "trace", "workflow"]

NODE_TYPE_VALUES: set[NodeType] = {"agent", "chain", "chat", "llm", "retriever", "session", "tool", "trace", "workflow"}


def check_node_type(value: str) -> NodeType:
    if value in NODE_TYPE_VALUES:
        return cast(NodeType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {NODE_TYPE_VALUES!r}")
