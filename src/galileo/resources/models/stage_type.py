from enum import Enum


class StageType(str, Enum):
    CENTRAL = "central"
    LOCAL = "local"

    def __str__(self) -> str:
        return str(self.value)
