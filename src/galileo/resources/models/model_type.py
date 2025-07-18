from enum import Enum


class ModelType(str, Enum):
    CODE = "code"
    LLM = "llm"
    SLM = "slm"

    def __str__(self) -> str:
        return str(self.value)
