from enum import Enum


class OrganizationAction(str, Enum):
    DELETE = "delete"
    DELETE_LOG_DATA = "delete_log_data"
    READ_COST_SETTINGS = "read_cost_settings"
    READ_SETTINGS = "read_settings"
    RENAME = "rename"
    UPDATE_SETTINGS = "update_settings"

    def __str__(self) -> str:
        return str(self.value)
