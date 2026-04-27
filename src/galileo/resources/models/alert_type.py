from enum import Enum


class AlertType(str, Enum):
    MULTI_CONDITIONOBJECT1 = "multi_condition/object/1"

    def __str__(self) -> str:
        return str(self.value)
