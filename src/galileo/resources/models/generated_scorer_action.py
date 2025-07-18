from typing import Literal, cast

GeneratedScorerAction = Literal["delete", "update"]

GENERATED_SCORER_ACTION_VALUES: set[GeneratedScorerAction] = {"delete", "update"}


def check_generated_scorer_action(value: str) -> GeneratedScorerAction:
    if value in GENERATED_SCORER_ACTION_VALUES:
        return cast(GeneratedScorerAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GENERATED_SCORER_ACTION_VALUES!r}")
