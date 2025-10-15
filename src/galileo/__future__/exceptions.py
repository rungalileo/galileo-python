from typing import Optional


class GalileoFutureError(Exception):
    """
    Base exception for all Galileo Future API errors.

    This exception serves as the base class for all custom exceptions
    in the future API, allowing users to catch all API-related errors.
    """


class ConfigurationError(GalileoFutureError):
    """
    Raised when there are configuration-related errors.

    This includes missing API keys, invalid URLs, or connection failures.
    """


class ValidationError(GalileoFutureError):
    """
    Raised when input validation fails.

    This includes invalid parameter combinations, missing required fields,
    or malformed input data.
    """


class ResourceNotFoundError(GalileoFutureError):
    """
    Raised when a requested resource cannot be found.

    This includes projects, datasets, prompts, or log streams that don't exist.
    """


class ResourceConflictError(GalileoFutureError):
    """
    Raised when there's a conflict with existing resources.

    This includes attempting to create resources with duplicate names
    or conflicting operations.
    """


class APIError(GalileoFutureError):
    """
    Raised when the underlying API returns an error.

    This wraps errors from the legacy API to provide consistent error handling.
    """

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error
