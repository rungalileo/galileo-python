from enum import Enum


class RootType(str, Enum):
    SESSION = "session"
    SPAN = "span"
    TRACE = "trace"

    def __str__(self) -> str:
        return str(self.value)
