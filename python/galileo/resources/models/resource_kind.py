from enum import Enum


class ResourceKind(str, Enum):
    API_KEY = "api_key"
    DATASET = "dataset"
    GENERATED_SCORER = "generated_scorer"
    GROUP = "group"
    GROUP_MEMBER = "group_member"
    INTEGRATION = "integration"
    PROJECT = "project"
    REGISTERED_SCORER = "registered_scorer"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
