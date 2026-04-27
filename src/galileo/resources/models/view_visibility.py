from enum import Enum


class ViewVisibility(str, Enum):
    PROJECT = "project"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
