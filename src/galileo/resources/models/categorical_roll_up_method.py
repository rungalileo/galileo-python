from enum import Enum


class CategoricalRollUpMethod(str, Enum):
    CATEGORY_COUNT = "category_count"

    def __str__(self) -> str:
        return str(self.value)
