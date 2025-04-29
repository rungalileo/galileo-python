from enum import Enum


class StepType(str, Enum):
    LLM = "llm"
    RETRIEVER = "retriever"
    TOOL = "tool"
    TRACE = "trace"
    WORKFLOW = "workflow"

    def __str__(self) -> str:
        return str(self.value)
