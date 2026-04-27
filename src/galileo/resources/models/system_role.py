from enum import Enum


class SystemRole(str, Enum):
    SYSTEM_ADMIN = "system_admin"
    SYSTEM_USER = "system_user"

    def __str__(self) -> str:
        return str(self.value)
