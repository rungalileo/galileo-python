from enum import Enum


class CodeMetricGenerationStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    GENERATING = "generating"

    def __str__(self) -> str:
        return str(self.value)
