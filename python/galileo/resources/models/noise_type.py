from enum import Enum


class NoiseType(str, Enum):
    FEATURE_NOISE = "Feature Noise"
    LABEL_NOISE = "Label Noise"
    NONE = "None"

    def __str__(self) -> str:
        return str(self.value)
