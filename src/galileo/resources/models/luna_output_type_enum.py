from enum import Enum


class LunaOutputTypeEnum(str, Enum):
    FLOAT = "float"
    STRING = "string"
    STRING_LIST = "string_list"

    def __str__(self) -> str:
        return str(self.value)
