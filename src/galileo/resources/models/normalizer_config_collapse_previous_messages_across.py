from enum import Enum


class NormalizerConfigCollapsePreviousMessagesAcross(str, Enum):
    SESSION = "session"
    TRACE = "trace"

    def __str__(self) -> str:
        return str(self.value)
