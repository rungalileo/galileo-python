from enum import Enum


class OutputTypeEnum(str, Enum):
    BOOLEAN = "boolean"
    CATEGORICAL = "categorical"
    COUNT = "count"
    DISCRETE = "discrete"
    FREEFORM = "freeform"
    PERCENTAGE = "percentage"

    def __str__(self) -> str:
        return str(self.value)
