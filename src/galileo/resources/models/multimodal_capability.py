from enum import Enum


class MultimodalCapability(str, Enum):
    AUDIO = "audio"
    VISION = "vision"

    def __str__(self) -> str:
        return str(self.value)
