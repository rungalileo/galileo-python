from enum import Enum


class Operator(str, Enum):
    BETWEEN = "between"
    CONTAINS = "contains"
    EQ = "eq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    NE = "ne"
    NOT_IN = "not_in"
    ONE_OF = "one_of"

    def __str__(self) -> str:
        return str(self.value)
