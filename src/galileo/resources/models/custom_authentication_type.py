from enum import Enum


class CustomAuthenticationType(str, Enum):
    API_KEY = "api_key"
    NONE = "none"
    OAUTH2 = "oauth2"

    def __str__(self) -> str:
        return str(self.value)
