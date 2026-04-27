from enum import Enum


class NormalizerConfigCollapseToolsAcross(str, Enum):
    SESSION = "session"
    TRACE = "trace"

    def __str__(self) -> str:
        return str(self.value)
