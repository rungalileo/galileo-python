from enum import Enum


class ControlAction(str, Enum):
    DENY = "deny"
    OBSERVE = "observe"
    STEER = "steer"

    def __str__(self) -> str:
        return str(self.value)
