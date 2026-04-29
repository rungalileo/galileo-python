from enum import Enum


class LogRecordsFilterType(str, Enum):
    BOOLEAN = "boolean"
    COLLECTION = "collection"
    DATE = "date"
    FULLY_ANNOTATED = "fully_annotated"
    ID = "id"
    NUMBER = "number"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
