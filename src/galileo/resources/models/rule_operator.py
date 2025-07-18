from enum import Enum


class RuleOperator(str, Enum):
    ALL = "all"
    ANY = "any"
    CONTAINS = "contains"
    EMPTY = "empty"
    EQ = "eq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    NEQ = "neq"
    NOT_EMPTY = "not_empty"

    def __str__(self) -> str:
        return str(self.value)
