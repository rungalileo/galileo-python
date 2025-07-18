from typing import Literal, cast

LoggingMethod = Literal["api_direct", "playground", "python_client", "typescript_client"]

LOGGING_METHOD_VALUES: set[LoggingMethod] = {"api_direct", "playground", "python_client", "typescript_client"}


def check_logging_method(value: str) -> LoggingMethod:
    if value in LOGGING_METHOD_VALUES:
        return cast(LoggingMethod, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOGGING_METHOD_VALUES!r}")
