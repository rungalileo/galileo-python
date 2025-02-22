from enum import Enum


class DatasetAction(str, Enum):
    DELETE = "delete"
    EXPORT = "export"
    RENAME = "rename"
    SHARE = "share"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
