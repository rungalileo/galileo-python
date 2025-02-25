from enum import Enum


class ChunkAttributionUtilizationScorerType(str, Enum):
    LUNA = "luna"
    PLUS = "plus"

    def __str__(self) -> str:
        return str(self.value)
