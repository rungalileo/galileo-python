from enum import Enum


class ProjectLabels(str, Enum):
    SAMPLE = "sample"

    def __str__(self) -> str:
        return str(self.value)
