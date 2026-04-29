from enum import Enum


class ControlAppliesTo(str, Enum):
    LLM_CALL = "llm_call"
    TOOL_CALL = "tool_call"

    def __str__(self) -> str:
        return str(self.value)
