from typing import Literal, cast

ActionType = Literal["OVERRIDE", "PASSTHROUGH"]

ACTION_TYPE_VALUES: set[ActionType] = {"OVERRIDE", "PASSTHROUGH"}


def check_action_type(value: str) -> ActionType:
    if value in ACTION_TYPE_VALUES:
        return cast(ActionType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ACTION_TYPE_VALUES!r}")
