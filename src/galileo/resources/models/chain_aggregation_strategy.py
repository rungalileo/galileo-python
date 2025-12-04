from enum import Enum


class ChainAggregationStrategy(str, Enum):
    AVERAGE = "average"
    FIRST = "first"
    LAST = "last"
    SUM = "sum"

    def __str__(self) -> str:
        return str(self.value)
