from enum import Enum


class GroupMemberAction(str, Enum):
    DELETE = "delete"
    UPDATE_ROLE = "update_role"

    def __str__(self) -> str:
        return str(self.value)
