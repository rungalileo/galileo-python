from enum import Enum


class ModelCostBy(str, Enum):
    CHARACTERS = "characters"
    TOKENS = "tokens"

    def __str__(self) -> str:
        return str(self.value)
