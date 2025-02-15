from enum import Enum


class SemSegErrorType(str, Enum):
    BACKGROUND = "background"
    CLASSIFICATION = "classification"
    CLASS_CONFUSION = "class_confusion"
    MISSED = "missed"
    NONE = "None"

    def __str__(self) -> str:
        return str(self.value)
