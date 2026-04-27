from enum import Enum


class GroupVisibility(str, Enum):
    HIDDEN = "hidden"
    PRIVATE = "private"
    PROTECTED = "protected"
    PUBLIC = "public"

    def __str__(self) -> str:
        return str(self.value)
