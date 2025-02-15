from enum import Enum


class AwsCredentialType(str, Enum):
    ASSUMED_ROLE = "assumed_role"
    KEY_SECRET = "key_secret"

    def __str__(self) -> str:
        return str(self.value)
