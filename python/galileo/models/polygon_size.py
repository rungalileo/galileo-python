from enum import Enum


class PolygonSize(str, Enum):
    EXTRA_LARGE = "extra_large"
    EXTRA_SMALL = "extra_small"
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"

    def __str__(self) -> str:
        return str(self.value)
