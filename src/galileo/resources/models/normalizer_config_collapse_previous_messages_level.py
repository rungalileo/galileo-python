from enum import Enum


class NormalizerConfigCollapsePreviousMessagesLevel(str, Enum):
    SESSION = "session"
    TRACE = "trace"

    def __str__(self) -> str:
        return str(self.value)
