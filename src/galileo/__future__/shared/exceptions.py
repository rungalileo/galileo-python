from typing import ClassVar, Optional


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


class SyncError(GalileoFutureError):
    """
    Raised when there's a state synchronization error.

    This includes failures to persist changes, conflicts during updates,
    or other synchronization-related issues.
    """

    def __init__(self, message: str, sync_state: Optional[str] = None, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.sync_state = sync_state
        self.original_error = original_error


class IntegrationNotConfiguredError(GalileoFutureError):
    """
    Raised when attempting to use an integration that is not configured.

    This error provides guidance on how to create or configure the integration.
    """

    # Integrations that have SDK create methods
    _SUPPORTED_CREATE_METHODS: ClassVar[dict[str, str]] = {
        "openai": "Integration.create_openai()",
        "azure": "Integration.create_azure()",
        "aws_bedrock": "Integration.create_bedrock()",
        "anthropic": "Integration.create_anthropic()",
    }

    def __init__(self, integration_name: str):
        create_method = self._SUPPORTED_CREATE_METHODS.get(integration_name)
        if create_method:
            message = (
                f"No '{integration_name}' integration configured.\n"
                f"Create one using {create_method} or configure it in the Galileo console."
            )
        else:
            message = f"No '{integration_name}' integration configured.\nConfigure it in the Galileo console."
        super().__init__(message)
        self.integration_name = integration_name
