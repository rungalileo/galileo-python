from enum import Enum


class Split(str, Enum):
    INFERENCE = "inference"
    TEST = "test"
    TRAINING = "training"
    VALIDATION = "validation"

    def __str__(self) -> str:
        return str(self.value)
