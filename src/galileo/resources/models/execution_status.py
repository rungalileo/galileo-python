from enum import Enum
from typing import Optional


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
    def _missing_(cls, value: object) -> Optional["ExecutionStatus"]:
        if isinstance(value, str):
            for member in cls:
                if member.value == value.lower():
                    return member
        return None
