from enum import Enum


class ScorerType(str, Enum):
    LUNA = "Luna"
    PLUS = "Plus"

    def __str__(self) -> str:
        return str(self.value)
