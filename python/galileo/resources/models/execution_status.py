from enum import Enum


class ExecutionStatus(str, Enum):
    ERROR = "error"
    FAILED = "failed"
    NOT_TRIGGERED = "not_triggered"
    PAUSED = "paused"
    TIMEOUT = "timeout"
    TRIGGERED = "triggered"

    def __str__(self) -> str:
        return str(self.value)
