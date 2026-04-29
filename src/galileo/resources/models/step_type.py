from enum import Enum


class StepType(str, Enum):
    AGENT = "agent"
    LLM = "llm"
    RETRIEVER = "retriever"
    SESSION = "session"
    TOOL = "tool"
    TRACE = "trace"
    WORKFLOW = "workflow"

    def __str__(self) -> str:
        return str(self.value)
