from typing import Literal, cast

ScorerTagsFilterOperator = Literal["contains", "not_in"]

SCORER_TAGS_FILTER_OPERATOR_VALUES: set[ScorerTagsFilterOperator] = {"contains", "not_in"}


def check_scorer_tags_filter_operator(value: str) -> ScorerTagsFilterOperator:
    if value in SCORER_TAGS_FILTER_OPERATOR_VALUES:
        return cast(ScorerTagsFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SCORER_TAGS_FILTER_OPERATOR_VALUES!r}")
