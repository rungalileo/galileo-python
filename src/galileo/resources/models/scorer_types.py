from enum import Enum


class ScorerTypes(str, Enum):
    CODE = "code"
    DECISION = "decision"
    LLM = "llm"
    LUNA = "luna"
    PRESET = "preset"

    def __str__(self) -> str:
        return str(self.value)
