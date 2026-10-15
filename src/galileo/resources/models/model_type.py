from enum import Enum


class ModelType(str, Enum):
    CODE = "code"
    DECISION = "decision"
    LLM = "llm"
    SLM = "slm"

    def __str__(self) -> str:
        return str(self.value)
