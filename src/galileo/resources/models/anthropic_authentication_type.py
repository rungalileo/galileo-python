from enum import Enum


class AnthropicAuthenticationType(str, Enum):
    API_KEY = "api_key"
    CUSTOM_OAUTH2 = "custom_oauth2"

    def __str__(self) -> str:
        return str(self.value)
