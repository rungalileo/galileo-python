"""
Galileo Future API.

This package provides the next-generation object-centric API for Galileo.
"""

from galileo.__future__.configuration import Configuration
from galileo.__future__.exceptions import (
    APIError,
    ConfigurationError,
    GalileoFutureError,
    ResourceConflictError,
    ResourceNotFoundError,
    ValidationError,
)
from galileo.utils.logging import enable_console_logging

__all__ = [
    "APIError",
    "Configuration",
    "ConfigurationError",
    "GalileoFutureError",
    "ResourceConflictError",
    "ResourceNotFoundError",
    "ValidationError",
    "enable_console_logging",
]
