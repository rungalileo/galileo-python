from enum import Enum


class CategoryFilterOperator(str, Enum):
    ALL = "all"
    ANY = "any"
    EXACT = "exact"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
