from enum import Enum


class LogDataSort(str, Enum):
    STANDARD = "standard"

    def __str__(self) -> str:
        return str(self.value)
