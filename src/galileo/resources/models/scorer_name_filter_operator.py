from typing import Literal, cast

ScorerNameFilterOperator = Literal["contains", "eq", "ne", "not_in", "one_of"]

SCORER_NAME_FILTER_OPERATOR_VALUES: set[ScorerNameFilterOperator] = {"contains", "eq", "ne", "not_in", "one_of"}


def check_scorer_name_filter_operator(value: str) -> ScorerNameFilterOperator:
    if value in SCORER_NAME_FILTER_OPERATOR_VALUES:
        return cast(ScorerNameFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SCORER_NAME_FILTER_OPERATOR_VALUES!r}")
