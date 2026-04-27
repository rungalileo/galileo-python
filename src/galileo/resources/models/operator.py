from enum import Enum


class Operator(str, Enum):
    BETWEEN = "between"
    CONTAINS = "contains"
    EQ = "eq"
    GT = "gt"
    GTE = "gte"
    HAS_ALL = "has_all"
    IN = "in"
    LIKE = "like"
    LT = "lt"
    LTE = "lte"
    NE = "ne"
    NOT_IN = "not_in"

    def __str__(self) -> str:
        return str(self.value)
