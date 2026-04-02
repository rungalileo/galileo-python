from enum import Enum


class AuthMethod(str, Enum):
    AZURE_AD = "azure-ad"
    CUSTOM = "custom"
    EMAIL = "email"
    GITHUB = "github"
    GOOGLE = "google"
    OKTA = "okta"
    SAML = "saml"

    def __str__(self) -> str:
        return str(self.value)
