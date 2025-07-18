from typing import Literal, cast

OrganizationAction = Literal["delete", "rename"]

ORGANIZATION_ACTION_VALUES: set[OrganizationAction] = {"delete", "rename"}


def check_organization_action(value: str) -> OrganizationAction:
    if value in ORGANIZATION_ACTION_VALUES:
        return cast(OrganizationAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ORGANIZATION_ACTION_VALUES!r}")
