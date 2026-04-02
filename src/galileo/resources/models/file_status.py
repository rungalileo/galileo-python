from enum import Enum


class FileStatus(str, Enum):
    COMPLETE = "complete"
    FAILED = "failed"
    NOT_UPLOADED = "not_uploaded"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
