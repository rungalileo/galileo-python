from enum import Enum


class AzureAuthenticationType(str, Enum):
    API_KEY = "api_key"
    CLIENT_SECRET = "client_secret"
    CUSTOM_OAUTH2 = "custom_oauth2"
    USERNAME_PASSWORD = "username_password"

    def __str__(self) -> str:
        return str(self.value)
