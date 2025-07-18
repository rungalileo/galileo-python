from typing import Literal, cast

ScorerCreatedAtFilterOperator = Literal["eq", "gt", "gte", "lt", "lte", "ne"]

SCORER_CREATED_AT_FILTER_OPERATOR_VALUES: set[ScorerCreatedAtFilterOperator] = {"eq", "gt", "gte", "lt", "lte", "ne"}


def check_scorer_created_at_filter_operator(value: str) -> ScorerCreatedAtFilterOperator:
    if value in SCORER_CREATED_AT_FILTER_OPERATOR_VALUES:
        return cast(ScorerCreatedAtFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SCORER_CREATED_AT_FILTER_OPERATOR_VALUES!r}")
