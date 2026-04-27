from enum import Enum


class QueueAction(str, Enum):
    ABORT = "abort"
    COMPLETE = "complete"

    def __str__(self) -> str:
        return str(self.value)
