from enum import Enum


class IntegrationAction(str, Enum):
    DELETE = "delete"
    READ_SECRETS = "read_secrets"
    SHARE = "share"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
