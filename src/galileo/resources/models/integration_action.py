from typing import Literal, cast

IntegrationAction = Literal["delete", "share", "update"]

INTEGRATION_ACTION_VALUES: set[IntegrationAction] = {"delete", "share", "update"}


def check_integration_action(value: str) -> IntegrationAction:
    if value in INTEGRATION_ACTION_VALUES:
        return cast(IntegrationAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INTEGRATION_ACTION_VALUES!r}")
