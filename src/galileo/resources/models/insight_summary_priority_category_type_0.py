from enum import Enum


class InsightSummaryPriorityCategoryType0(str, Enum):
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
