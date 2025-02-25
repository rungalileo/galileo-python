from enum import Enum


class AzureAuthenticationType(str, Enum):
    API_KEY = "api_key"
    CLIENT_SECRET = "client_secret"
    USERNAME_PASSWORD = "username_password"

    def __str__(self) -> str:
        return str(self.value)
