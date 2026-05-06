from enum import Enum


class LunaOutputTypeEnum(str, Enum):
    BOOL_LIST = "bool_list"
    FLOAT = "float"
    STRING = "string"
    STRING_LIST = "string_list"

    def __str__(self) -> str:
        return str(self.value)
