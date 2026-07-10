from enum import Enum


class ScorerMultimodalCapabilitiesFilterOperator(str, Enum):
    CONTAINS = "contains"
    EQ = "eq"
    NOT_IN = "not_in"
    ONE_OF = "one_of"

    def __str__(self) -> str:
        return str(self.value)
