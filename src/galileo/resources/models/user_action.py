from enum import Enum


class UserAction(str, Enum):
    CHANGE_ROLE_TO_ADMIN = "change_role_to_admin"
    CHANGE_ROLE_TO_MANAGER = "change_role_to_manager"
    CHANGE_ROLE_TO_READ_ONLY = "change_role_to_read_only"
    CHANGE_ROLE_TO_USER = "change_role_to_user"
    DELETE = "delete"
    READ_API_KEYS = "read_api_keys"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
