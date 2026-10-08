from enum import Enum


class ControlAppliesTo(str, Enum):
    LLM_CALL = "llm_call"
    RETRIEVER_CALL = "retriever_call"
    SESSION_CALL = "session_call"
    TOOL_CALL = "tool_call"
    TRACE_CALL = "trace_call"

    def __str__(self) -> str:
        return str(self.value)
