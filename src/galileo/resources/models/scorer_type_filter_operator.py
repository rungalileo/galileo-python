from typing import Literal, cast

ScorerTypeFilterOperator = Literal["eq", "ne", "not_in", "one_of"]

SCORER_TYPE_FILTER_OPERATOR_VALUES: set[ScorerTypeFilterOperator] = {"eq", "ne", "not_in", "one_of"}


def check_scorer_type_filter_operator(value: str) -> ScorerTypeFilterOperator:
    if value in SCORER_TYPE_FILTER_OPERATOR_VALUES:
        return cast(ScorerTypeFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SCORER_TYPE_FILTER_OPERATOR_VALUES!r}")
