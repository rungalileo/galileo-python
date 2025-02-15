from enum import Enum


class ApiKeyAction(str, Enum):
    DELETE = "delete"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
