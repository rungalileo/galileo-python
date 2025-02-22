from enum import Enum


class GroupAction(str, Enum):
    JOIN = "join"
    LIST_MEMBERS = "list_members"
    REQUEST_TO_JOIN = "request_to_join"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
