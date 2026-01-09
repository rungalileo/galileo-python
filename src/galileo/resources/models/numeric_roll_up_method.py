from enum import Enum


class NumericRollUpMethod(str, Enum):
    AVERAGE = "average"
    MAX = "max"
    MIN = "min"
    SUM = "sum"

    def __str__(self) -> str:
        return str(self.value)
