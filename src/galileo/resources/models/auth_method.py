from typing import Literal, cast

AuthMethod = Literal["azure-ad", "custom", "email", "github", "google", "okta"]

AUTH_METHOD_VALUES: set[AuthMethod] = {"azure-ad", "custom", "email", "github", "google", "okta"}


def check_auth_method(value: str) -> AuthMethod:
    if value in AUTH_METHOD_VALUES:
        return cast(AuthMethod, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_METHOD_VALUES!r}")
