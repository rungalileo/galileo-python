from typing import Literal, cast

ApiKeyAction = Literal["delete", "update"]

API_KEY_ACTION_VALUES: set[ApiKeyAction] = {"delete", "update"}


def check_api_key_action(value: str) -> ApiKeyAction:
    if value in API_KEY_ACTION_VALUES:
        return cast(ApiKeyAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {API_KEY_ACTION_VALUES!r}")
