from enum import Enum


class GenericAction(str, Enum):
    GENERIC_CREATE = "generic_create"
    GENERIC_DELETE = "generic_delete"
    GENERIC_READ = "generic_read"
    GENERIC_UPDATE = "generic_update"

    def __str__(self) -> str:
        return str(self.value)
