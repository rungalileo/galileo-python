from enum import Enum


class LogRecordsColumnInfoLabelColorType0(str, Enum):
    NEGATIVE = "negative"
    POSITIVE = "positive"

    def __str__(self) -> str:
        return str(self.value)
