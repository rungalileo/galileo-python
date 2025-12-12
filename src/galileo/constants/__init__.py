from typing import Literal

DEFAULT_PROJECT_NAME = "default"
DEFAULT_LOG_STREAM_NAME = "default"
DEFAULT_MODE = "batch"

DEFAULT_API_URL = "https://api.galileo.ai/"

# HTTP header prefix for all Galileo headers
GALILEO_HEADER_PREFIX = "X-Galileo"

# Type definitions
LoggerModeType = Literal["batch", "distributed"]

__all__ = (
    "DEFAULT_API_URL",
    "DEFAULT_LOG_STREAM_NAME",
    "DEFAULT_MODE",
    "DEFAULT_PROJECT_NAME",
    "GALILEO_HEADER_PREFIX",
    "LoggerModeType",
)
