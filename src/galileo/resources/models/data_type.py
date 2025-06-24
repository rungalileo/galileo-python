from enum import Enum


class DataType(str, Enum):
    BOOLEAN = "boolean"
    FLOATING_POINT = "floating_point"
    INTEGER = "integer"
    STRING_LIST = "string_list"
    TEXT = "text"
    TIMESTAMP = "timestamp"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
