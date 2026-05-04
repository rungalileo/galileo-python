from typing import ClassVar

from galileo.exceptions import NotFoundError
from galileo.utils.env_helpers import _get_project_from_env, _get_project_id_from_env


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


class ResourceNotFoundError(NotFoundError, GalileoFutureError):
    """
    Backward-compatible alias for NotFoundError.

    Raised when a requested resource cannot be found.
    New code should catch NotFoundError instead.
    """

    def __init__(self, message: str):
        NotFoundError.__init__(self, message)


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

    def __init__(self, message: str, original_error: Exception | None = None):
        super().__init__(message)
        self.original_error = original_error


class SyncError(GalileoFutureError):
    """
    Raised when there's a state synchronization error.

    This includes failures to persist changes, conflicts during updates,
    or other synchronization-related issues.
    """

    def __init__(self, message: str, sync_state: str | None = None, original_error: Exception | None = None):
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


def _project_not_found_error(project_id: str | None, project_name: str | None) -> "NotFoundError":
    """Return a context-aware NotFoundError for a missing project.

    Distinguishes between "a name/id was given but the project doesn't exist" (actionable: create it)
    and "no identifier was specified at all" (actionable: provide one).
    Falls back to env vars so the message is accurate even when the identifier came from the environment.
    """
    effective_id = project_id or _get_project_id_from_env()
    effective_name = project_name or (None if effective_id else _get_project_from_env())
    if effective_name:
        return NotFoundError(
            f'Project "{effective_name}" not found. '
            f'Use Project(name="{effective_name}").create() or the Galileo UI to create it first.'
        )
    if effective_id:
        return NotFoundError(
            f'Project with id "{effective_id}" not found. '
            "Use Project(name=...).create() or the Galileo UI to create a project first."
        )
    return NotFoundError("No project specified. Provide project_id, project_name, or set GALILEO_PROJECT env var.")
