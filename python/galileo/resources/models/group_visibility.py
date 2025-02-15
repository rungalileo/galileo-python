from enum import Enum


class GroupVisibility(str, Enum):
    HIDDEN = "hidden"
    PRIVATE = "private"
    PUBLIC = "public"

    def __str__(self) -> str:
        return str(self.value)
