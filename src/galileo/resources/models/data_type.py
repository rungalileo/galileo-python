from enum import Enum


class DataType(str, Enum):
    BOOLEAN = "boolean"
    DATASET = "dataset"
    FLOATING_POINT = "floating_point"
    INTEGER = "integer"
    PLAYGROUND = "playground"
    PROMPT = "prompt"
    RANK = "rank"
    STRING_LIST = "string_list"
    TAG = "tag"
    TEXT = "text"
    TIMESTAMP = "timestamp"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
