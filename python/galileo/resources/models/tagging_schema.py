from enum import Enum


class TaggingSchema(str, Enum):
    BILOU = "BILOU"
    BIO = "BIO"
    BIOES = "BIOES"

    def __str__(self) -> str:
        return str(self.value)
