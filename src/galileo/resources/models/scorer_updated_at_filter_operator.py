from typing import Literal, cast

ScorerUpdatedAtFilterOperator = Literal["eq", "gt", "gte", "lt", "lte", "ne"]

SCORER_UPDATED_AT_FILTER_OPERATOR_VALUES: set[ScorerUpdatedAtFilterOperator] = {"eq", "gt", "gte", "lt", "lte", "ne"}


def check_scorer_updated_at_filter_operator(value: str) -> ScorerUpdatedAtFilterOperator:
    if value in SCORER_UPDATED_AT_FILTER_OPERATOR_VALUES:
        return cast(ScorerUpdatedAtFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SCORER_UPDATED_AT_FILTER_OPERATOR_VALUES!r}")
