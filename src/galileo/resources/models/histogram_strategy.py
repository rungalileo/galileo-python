from enum import Enum


class HistogramStrategy(str, Enum):
    FIXED = "fixed"
    QUANTILE = "quantile"
    TRIMMED = "trimmed"

    def __str__(self) -> str:
        return str(self.value)
