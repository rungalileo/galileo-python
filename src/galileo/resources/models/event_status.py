from enum import Enum


class EventStatus(str, Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    INCOMPLETE = "incomplete"
    IN_PROGRESS = "in_progress"

    def __str__(self) -> str:
        return str(self.value)
