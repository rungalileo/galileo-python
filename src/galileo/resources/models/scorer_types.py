from typing import Literal, cast

ScorerTypes = Literal["code", "llm", "preset"]

SCORER_TYPES_VALUES: set[ScorerTypes] = {"code", "llm", "preset"}


def check_scorer_types(value: str) -> ScorerTypes:
    if value in SCORER_TYPES_VALUES:
        return cast(ScorerTypes, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SCORER_TYPES_VALUES!r}")
