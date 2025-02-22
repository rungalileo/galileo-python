from enum import Enum


class UsagePlanName(str, Enum):
    DEVELOPER = "developer"
    ENTERPRISE = "enterprise"
    PRO = "pro"

    def __str__(self) -> str:
        return str(self.value)
