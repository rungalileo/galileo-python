from enum import Enum


class InsightType(str, Enum):
    HORIZONTAL_BAR = "horizontal_bar"
    VERTICAL_BAR = "vertical_bar"

    def __str__(self) -> str:
        return str(self.value)
