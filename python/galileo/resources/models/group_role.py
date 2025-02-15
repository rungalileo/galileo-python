from enum import Enum


class GroupRole(str, Enum):
    MAINTAINER = "maintainer"
    MEMBER = "member"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
