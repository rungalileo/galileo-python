from enum import Enum


class FieldType(str, Enum):
    ARRAY = "array"
    BOOL = "bool"
    FLOAT = "float"
    INT = "int"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
