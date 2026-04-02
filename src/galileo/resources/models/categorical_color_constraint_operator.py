from enum import Enum


class CategoricalColorConstraintOperator(str, Enum):
    EQ = "eq"
    ONE_OF = "one_of"

    def __str__(self) -> str:
        return str(self.value)
