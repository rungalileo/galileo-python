from enum import Enum


class LogDataLoggingMethod(str, Enum):
    API_DIRECT = "api_direct"
    PYTHON_CLIENT = "python_client"
    TYPESCRIPT_CLIENT = "typescript_client"

    def __str__(self) -> str:
        return str(self.value)
