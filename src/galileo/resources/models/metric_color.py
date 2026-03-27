from enum import Enum


class MetricColor(str, Enum):
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"

    def __str__(self) -> str:
        return str(self.value)
