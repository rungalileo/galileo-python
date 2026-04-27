from enum import Enum


class SystemUserStatus(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    INVITED = "invited"
    REQUESTED = "requested"

    def __str__(self) -> str:
        return str(self.value)
