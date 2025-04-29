from enum import Enum


class DataUnit(str, Enum):
    COUNT_AND_TOTAL = "count_and_total"
    DOLLARS = "dollars"
    MILLI_SECONDS = "milli_seconds"
    NANO_SECONDS = "nano_seconds"
    PERCENTAGE = "percentage"

    def __str__(self) -> str:
        return str(self.value)
