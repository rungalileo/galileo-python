from enum import Enum


class ScorerFeedbackQueueStatus(str, Enum):
    COMPLETED = "completed"
    GENERATING = "generating"
    PENDING = "pending"
    REVIEWING = "reviewing"

    def __str__(self) -> str:
        return str(self.value)
