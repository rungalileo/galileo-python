from enum import Enum


class NodeType(str, Enum):
    AGENT = "agent"
    CHAIN = "chain"
    CHAT = "chat"
    LLM = "llm"
    RETRIEVER = "retriever"
    SESSION = "session"
    TOOL = "tool"
    TRACE = "trace"
    WORKFLOW = "workflow"

    def __str__(self) -> str:
        return str(self.value)
