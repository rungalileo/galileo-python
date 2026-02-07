from enum import Enum


class InputModality(str, Enum):
    AUDIO = "audio"
    DOCUMENT = "document"
    IMAGE = "image"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
