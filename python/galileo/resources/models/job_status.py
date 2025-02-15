from enum import Enum


class JobStatus(str, Enum):
    COMPLETED = "completed"
    ERROR = "error"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    UNSTARTED = "unstarted"

    def __str__(self) -> str:
        return str(self.value)
