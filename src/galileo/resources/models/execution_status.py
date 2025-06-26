from enum import Enum


class ExecutionStatus(str, Enum):
    ERROR = "error"
    FAILED = "failed"
    NOT_TRIGGERED = "not_triggered"
    PAUSED = "paused"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"
    TRIGGERED = "triggered"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            lower_value = value.lower()
            for member in cls:
                if member.value == lower_value:
                    return member
        return None
