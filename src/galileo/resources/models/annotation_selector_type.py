from enum import Enum


class AnnotationSelectorType(str, Enum):
    TRACES = "traces"

    def __str__(self) -> str:
        return str(self.value)
