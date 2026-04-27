from enum import Enum


class ResourceKind(str, Enum):
    ANNOTATION_QUEUE = "annotation_queue"
    API_KEY = "api_key"
    AUDIT_LOG = "audit_log"
    DATASET = "dataset"
    EXPERIMENT = "experiment"
    FINETUNED_SCORER = "finetuned_scorer"
    GENERATED_SCORER = "generated_scorer"
    GROUP = "group"
    GROUP_INTEGRATION = "group_integration"
    GROUP_MEMBER = "group_member"
    INTEGRATION = "integration"
    LOG_STREAM = "log_stream"
    ORGANIZATION = "organization"
    PROJECT = "project"
    PROMPT_TEMPLATE = "prompt_template"
    REGISTERED_SCORER = "registered_scorer"
    STAGE = "stage"
    STAGE_VERSION = "stage_version"
    SYSTEM_USER = "system_user"
    USAGE_LIMIT = "usage_limit"
    USER = "user"
    USER_INTEGRATION = "user_integration"
    USER_INTEGRATION_SELECTION = "user_integration_selection"

    def __str__(self) -> str:
        return str(self.value)
