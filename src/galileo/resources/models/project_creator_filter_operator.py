from enum import Enum


class ProjectCreatorFilterOperator(str, Enum):
    EQ = "eq"
    NE = "ne"

    def __str__(self) -> str:
        return str(self.value)
