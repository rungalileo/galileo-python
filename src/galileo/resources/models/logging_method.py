from enum import Enum


class LoggingMethod(str, Enum):
    API_DIRECT = "api_direct"
    PLAYGROUND = "playground"
    PYTHON_CLIENT = "python_client"
    TYPESCRIPT_CLIENT = "typescript_client"

    def __str__(self) -> str:
        return str(self.value)
