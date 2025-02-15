from enum import Enum


class ScorerTypeFilterOperator(str, Enum):
    EQ = "eq"
    NE = "ne"
    NOT_IN = "not_in"
    ONE_OF = "one_of"

    def __str__(self) -> str:
        return str(self.value)
