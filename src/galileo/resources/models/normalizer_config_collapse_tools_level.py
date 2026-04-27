from enum import Enum


class NormalizerConfigCollapseToolsLevel(str, Enum):
    SESSION = "session"
    TRACE = "trace"

    def __str__(self) -> str:
        return str(self.value)
