from enum import Enum


class MetricComputationStatus(str, Enum):
    ERROR = "error"
    FAILED = "failed"
    SUCCESS = "success"
    TIMEOUT = "timeout"

    def __str__(self) -> str:
        return str(self.value)
