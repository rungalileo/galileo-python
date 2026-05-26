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


def _normalize_identifier(value: str | None) -> str | None:
    """Strip and return ``None`` for empty/whitespace-only inputs.

    Mirrors the trimming :meth:`galileo.projects.Projects.get` does internally,
    so callers that pre-check identifiers see the same "effectively empty"
    values the API client would see.
    """
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _resolve_project_identifiers(project_id: str | None, project_name: str | None) -> tuple[str | None, str | None]:
    """Apply env-fallback precedence to produce a normalized ``(id, name)`` tuple.

    Matches the precedence documented by :meth:`galileo.projects.Projects.get_with_env_fallbacks`
    exactly: explicit ``project_id`` > explicit ``project_name`` > ``GALILEO_PROJECT_ID``
    > ``GALILEO_PROJECT``. Once an id is chosen, name is dropped; once a name is chosen,
    env-id is *not* consulted (an explicit name suppresses env-id fallback).

    Whitespace-only values (explicit kwargs or env vars) are treated as missing, so
    ``" "`` follows the same path as ``None`` instead of leaking a raw ``ValueError``
    from the API client's internal strip-and-validate.

    Shared by :func:`_project_not_found_error` (uses the result for error-message
    context) and :func:`galileo.shared.project_resolver._resolve_project` (uses the
    result for both the pre-check and the actual API call).
    """
    explicit_id = _normalize_identifier(project_id)
    if explicit_id:
        return explicit_id, None
    explicit_name = _normalize_identifier(project_name)
    if explicit_name:
        return None, explicit_name
    env_id = _normalize_identifier(_get_project_id_from_env())
    if env_id:
        return env_id, None
    env_name = _normalize_identifier(_get_project_from_env())
    if env_name:
        return None, env_name
    return None, None


def _project_not_found_error(project_id: str | None, project_name: str | None) -> "ResourceNotFoundError":
    """Return a context-aware ResourceNotFoundError for a missing project.

    Distinguishes between "a name/id was given but the project doesn't exist" (actionable: create it)
    and "no identifier was specified at all" (actionable: provide one).
    Falls back to env vars so the message is accurate even when the identifier came from the environment.

    Whitespace-only values (explicit kwargs or env vars) are normalized to ``None`` so callers
    get the actionable "No project specified" message instead of an empty-quoted identifier
    like ``Project "   " not found``.

    Returns ``ResourceNotFoundError`` (a subclass of :class:`NotFoundError`) so callers using either
    ``except NotFoundError`` or ``except ResourceNotFoundError`` continue to work.
    """
    effective_id, effective_name = _resolve_project_identifiers(project_id, project_name)
    if effective_name:
        return ResourceNotFoundError(
            f'Project "{effective_name}" not found. '
            f'Use Project(name="{effective_name}").create() or the Galileo UI to create it first.'
        )
    if effective_id:
        return ResourceNotFoundError(
            f'Project with id "{effective_id}" not found. '
            "Use Project(name=...).create() or the Galileo UI to create a project first."
        )
    return ResourceNotFoundError(
        "No project specified. Provide project_id, project_name, or set GALILEO_PROJECT env var."
    )
