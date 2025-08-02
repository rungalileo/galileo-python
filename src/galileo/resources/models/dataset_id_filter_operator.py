from enum import Enum


class DatasetIDFilterOperator(str, Enum):
    EQ = "eq"
    NE = "ne"

    def __str__(self) -> str:
        return str(self.value)
