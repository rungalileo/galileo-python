from enum import Enum


class TransactionRecordStatus(str, Enum):
    PROCESSED = "processed"
    PROCESSING = "processing"
    UNPROCESSED = "unprocessed"

    def __str__(self) -> str:
        return str(self.value)
