from typing import Literal, cast

GroupAction = Literal["join", "list_members", "request_to_join", "update"]

GROUP_ACTION_VALUES: set[GroupAction] = {"join", "list_members", "request_to_join", "update"}


def check_group_action(value: str) -> GroupAction:
    if value in GROUP_ACTION_VALUES:
        return cast(GroupAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GROUP_ACTION_VALUES!r}")
