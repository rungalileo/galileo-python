from enum import Enum


class UsageLimitNames(str, Enum):
    ORGS_PER_USER = "orgs_per_user"
    TRACES_PER_MONTH = "traces_per_month"
    USERS_PER_ORG = "users_per_org"

    def __str__(self) -> str:
        return str(self.value)
