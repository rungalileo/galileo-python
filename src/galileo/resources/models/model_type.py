from enum import Enum


class ModelType(str, Enum):
    LLM = "llm"
    SLM = "slm"

    def __str__(self) -> str:
        return str(self.value)
