from enum import Enum


class ErrorType(str, Enum):
    CONFIGURATION_ERROR = "configuration_error"
    CREDENTIALS_ERROR = "credentials_error"
    DATA_VALIDATION_ERROR = "data_validation_error"
    LLM_API_ERROR = "llm_api_error"
    NOT_APPLICABLE_REASON = "not_applicable_reason"
    NOT_FOUND_ERROR = "not_found_error"
    PERMISSION_ERROR = "permission_error"
    SYSTEM_ERROR = "system_error"
    UNCATALOGED_ERROR = "uncataloged_error"
    WORKFLOW_ERROR = "workflow_error"

    def __str__(self) -> str:
        return str(self.value)
