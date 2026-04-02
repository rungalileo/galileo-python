from enum import Enum


class MetricAggregation(str, Enum):
    AVERAGE = "Average"
    COUNT = "Count"
    MAX = "Max"
    MIN = "Min"
    P50 = "P50"
    P90 = "P90"
    P95 = "P95"
    P99 = "P99"
    SUM = "Sum"

    def __str__(self) -> str:
        return str(self.value)
