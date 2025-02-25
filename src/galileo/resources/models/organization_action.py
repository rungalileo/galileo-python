from enum import Enum


class OrganizationAction(str, Enum):
    DELETE = "delete"
    RENAME = "rename"

    def __str__(self) -> str:
        return str(self.value)
