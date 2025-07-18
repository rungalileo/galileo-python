from typing import Literal, cast

ContextAdherenceScorerType = Literal["luna", "plus"]

CONTEXT_ADHERENCE_SCORER_TYPE_VALUES: set[ContextAdherenceScorerType] = {"luna", "plus"}


def check_context_adherence_scorer_type(value: str) -> ContextAdherenceScorerType:
    if value in CONTEXT_ADHERENCE_SCORER_TYPE_VALUES:
        return cast(ContextAdherenceScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CONTEXT_ADHERENCE_SCORER_TYPE_VALUES!r}")
