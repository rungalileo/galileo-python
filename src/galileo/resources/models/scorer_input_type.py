from enum import Enum


class ScorerInputType(str, Enum):
    BASIC = "basic"
    NORMALIZED = "normalized"

    def __str__(self) -> str:
        return str(self.value)
