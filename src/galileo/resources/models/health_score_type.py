from enum import Enum


class HealthScoreType(str, Enum):
    MACRO_F1 = "macro_f1"
    MAE = "mae"
    MICRO_F1 = "micro_f1"
    MSE = "mse"

    def __str__(self) -> str:
        return str(self.value)
