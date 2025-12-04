from enum import Enum


class RollUpStrategy(str, Enum):
    AVG = "avg"
    FIRST = "first"
    LAST = "last"
    NONE = "none"
    SUM = "sum"

    def __str__(self) -> str:
        return str(self.value)
