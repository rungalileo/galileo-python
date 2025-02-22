from enum import Enum


class UserAction(str, Enum):
    DELETE = "delete"
    READ_API_KEYS = "read_api_keys"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
