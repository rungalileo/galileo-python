from typing import Literal, cast

CompletenessScorerType = Literal["luna", "plus"]

COMPLETENESS_SCORER_TYPE_VALUES: set[CompletenessScorerType] = {"luna", "plus"}


def check_completeness_scorer_type(value: str) -> CompletenessScorerType:
    if value in COMPLETENESS_SCORER_TYPE_VALUES:
        return cast(CompletenessScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {COMPLETENESS_SCORER_TYPE_VALUES!r}")
