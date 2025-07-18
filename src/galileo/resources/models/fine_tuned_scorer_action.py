from typing import Literal, cast

FineTunedScorerAction = Literal["delete", "update"]

FINE_TUNED_SCORER_ACTION_VALUES: set[FineTunedScorerAction] = {"delete", "update"}


def check_fine_tuned_scorer_action(value: str) -> FineTunedScorerAction:
    if value in FINE_TUNED_SCORER_ACTION_VALUES:
        return cast(FineTunedScorerAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FINE_TUNED_SCORER_ACTION_VALUES!r}")
