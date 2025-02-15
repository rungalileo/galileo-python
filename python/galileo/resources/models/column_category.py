from enum import Enum


class ColumnCategory(str, Enum):
    METRIC = "metric"
    STANDARD = "standard"
    USER_METADATA = "user_metadata"

    def __str__(self) -> str:
        return str(self.value)
