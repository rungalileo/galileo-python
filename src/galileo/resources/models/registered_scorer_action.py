from typing import Literal, cast

RegisteredScorerAction = Literal["delete", "update"]

REGISTERED_SCORER_ACTION_VALUES: set[RegisteredScorerAction] = {"delete", "update"}


def check_registered_scorer_action(value: str) -> RegisteredScorerAction:
    if value in REGISTERED_SCORER_ACTION_VALUES:
        return cast(RegisteredScorerAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {REGISTERED_SCORER_ACTION_VALUES!r}")
