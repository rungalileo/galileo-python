from enum import Enum


class SocialProvider(str, Enum):
    AZURE_AD = "azure-ad"
    CUSTOM = "custom"
    GITHUB = "github"
    GOOGLE = "google"
    OKTA = "okta"
    SAML = "saml"

    def __str__(self) -> str:
        return str(self.value)
