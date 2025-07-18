from typing import Literal, cast

NodeNameFilterOperator = Literal["contains", "eq", "ne"]

NODE_NAME_FILTER_OPERATOR_VALUES: set[NodeNameFilterOperator] = {"contains", "eq", "ne"}


def check_node_name_filter_operator(value: str) -> NodeNameFilterOperator:
    if value in NODE_NAME_FILTER_OPERATOR_VALUES:
        return cast(NodeNameFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {NODE_NAME_FILTER_OPERATOR_VALUES!r}")
