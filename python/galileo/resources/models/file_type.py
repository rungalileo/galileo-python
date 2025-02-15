from enum import Enum


class FileType(str, Enum):
    ARROW = "arrow"
    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    ZIP = "zip"

    def __str__(self) -> str:
        return str(self.value)
