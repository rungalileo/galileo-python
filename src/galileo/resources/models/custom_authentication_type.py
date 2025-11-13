from enum import Enum


class CustomAuthenticationType(str, Enum):
    OAUTH2 = "oauth2"

    def __str__(self) -> str:
        return str(self.value)
