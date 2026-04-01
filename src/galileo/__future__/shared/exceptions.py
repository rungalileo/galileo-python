"""Deprecated: use galileo.shared.exceptions instead of galileo.__future__.shared.exceptions."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.shared.exceptions is deprecated. Use galileo.shared.exceptions instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.shared.exceptions import (  # noqa: E402
    APIError,
    ConfigurationError,
    GalileoFutureError,
    IntegrationNotConfiguredError,
    ResourceConflictError,
    ResourceNotFoundError,
    SyncError,
    ValidationError,
)

__all__ = [
    "APIError",
    "ConfigurationError",
    "GalileoFutureError",
    "IntegrationNotConfiguredError",
    "ResourceConflictError",
    "ResourceNotFoundError",
    "SyncError",
    "ValidationError",
]
