from enum import Enum


class SelectorType(str, Enum):
    INDEXES = "indexes"
    TRACES = "traces"

    def __str__(self) -> str:
        return str(self.value)
