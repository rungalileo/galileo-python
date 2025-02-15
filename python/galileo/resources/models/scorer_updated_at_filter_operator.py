from enum import Enum


class ScorerUpdatedAtFilterOperator(str, Enum):
    EQ = "eq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    NE = "ne"

    def __str__(self) -> str:
        return str(self.value)
