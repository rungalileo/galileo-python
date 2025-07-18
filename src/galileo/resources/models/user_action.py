from typing import Literal, cast

UserAction = Literal["delete", "read_api_keys", "update"]

USER_ACTION_VALUES: set[UserAction] = {"delete", "read_api_keys", "update"}


def check_user_action(value: str) -> UserAction:
    if value in USER_ACTION_VALUES:
        return cast(UserAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {USER_ACTION_VALUES!r}")
