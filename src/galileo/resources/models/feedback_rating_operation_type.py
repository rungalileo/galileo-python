from enum import Enum


class FeedbackRatingOperationType(str, Enum):
    CREATE = "create"
    DELETE = "delete"

    def __str__(self) -> str:
        return str(self.value)
