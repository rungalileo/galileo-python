from enum import Enum


class ScorerTagsFilterOperator(str, Enum):
    CONTAINS = "contains"
    NOT_IN = "not_in"

    def __str__(self) -> str:
        return str(self.value)
