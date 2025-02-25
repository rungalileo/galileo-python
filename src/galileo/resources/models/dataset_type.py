from enum import Enum


class DatasetType(str, Enum):
    INFERENCE = "inference"
    TRAINING = "training"

    def __str__(self) -> str:
        return str(self.value)
