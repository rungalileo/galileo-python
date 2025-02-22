from enum import Enum


class ActionType(str, Enum):
    OVERRIDE = "OVERRIDE"
    PASSTHROUGH = "PASSTHROUGH"

    def __str__(self) -> str:
        return str(self.value)
