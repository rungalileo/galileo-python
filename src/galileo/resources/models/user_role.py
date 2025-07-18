from typing import Literal, cast

UserRole = Literal["admin", "manager", "read_only", "user"]

USER_ROLE_VALUES: set[UserRole] = {"admin", "manager", "read_only", "user"}


def check_user_role(value: str) -> UserRole:
    if value in USER_ROLE_VALUES:
        return cast(UserRole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {USER_ROLE_VALUES!r}")
