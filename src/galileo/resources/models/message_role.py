from enum import Enum


class MessageRole(str, Enum):
    AGENT = "agent"
    ASSISTANT = "assistant"
    DEVELOPER = "developer"
    FUNCTION = "function"
    SYSTEM = "system"
    TOOL = "tool"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
