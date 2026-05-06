from enum import Enum


class RollUpMethodDisplayOptions(str, Enum):
    AVERAGE = "average"
    CATEGORY_COUNT = "category_count"
    MAX = "max"
    MIN = "min"
    PERCENTAGE_FALSE = "percentage_false"
    PERCENTAGE_TRUE = "percentage_true"
    SUM = "sum"

    def __str__(self) -> str:
        return str(self.value)
