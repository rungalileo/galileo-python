from typing import Literal, cast

ScorerType = Literal["Luna", "Plus"]

SCORER_TYPE_VALUES: set[ScorerType] = {"Luna", "Plus"}


def check_scorer_type(value: str) -> ScorerType:
    if value in SCORER_TYPE_VALUES:
        return cast(ScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SCORER_TYPE_VALUES!r}")
