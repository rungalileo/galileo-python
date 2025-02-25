from enum import Enum


class OrganizationNameFilterOperator(str, Enum):
    CONTAINS = "contains"
    EQ = "eq"
    NE = "ne"

    def __str__(self) -> str:
        return str(self.value)
