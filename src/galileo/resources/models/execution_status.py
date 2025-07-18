from typing import Literal, cast

ExecutionStatus = Literal["error", "failed", "not_triggered", "paused", "skipped", "timeout", "triggered"]

EXECUTION_STATUS_VALUES: set[ExecutionStatus] = {
    "error",
    "failed",
    "not_triggered",
    "paused",
    "skipped",
    "timeout",
    "triggered",
}


def check_execution_status(value: str) -> ExecutionStatus:
    if value in EXECUTION_STATUS_VALUES:
        return cast(ExecutionStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {EXECUTION_STATUS_VALUES!r}")
