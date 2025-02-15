from enum import Enum


class ModelKind(str, Enum):
    SETFIT = "setfit"
    TRANSFORMERS = "transformers"

    def __str__(self) -> str:
        return str(self.value)
