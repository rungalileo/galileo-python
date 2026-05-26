"""Galileo SDK exceptions."""

from typing import Any, overload

__all__ = [
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "ForbiddenError",
    "GalileoAPIError",
    "GalileoLoggerException",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
]

# Sentinel for "argument not provided" so the message overload of NotFoundError can
# reject _any_ explicit second argument (including ``b""``), not just non-empty bytes.
_UNSET: Any = object()


class GalileoLoggerException(Exception):
    """Exception raised by GalileoLogger."""


class GalileoAPIError(Exception):
    """Base class for Galileo API HTTP errors with actionable messages."""

    def __init__(self, status_code: int, content: bytes, message: str):
        self.status_code = status_code
        self.content = content
        self.message = message
        response_text = content.decode(errors="ignore")
        super().__init__(f"{message} (HTTP {status_code})\n\nResponse: {response_text}")


class BadRequestError(GalileoAPIError):
    """HTTP 400 - The request was malformed or invalid."""

    def __init__(self, status_code: int, content: bytes):
        super().__init__(status_code, content, "Bad request. Check your request parameters and body format.")


class AuthenticationError(GalileoAPIError):
    """HTTP 401 - Authentication failed."""

    def __init__(self, status_code: int, content: bytes):
        super().__init__(
            status_code,
            content,
            "Authentication failed. Check your API key is valid and not expired. "
            "Set via GALILEO_API_KEY environment variable or pass api_key= when initializing the client.",
        )


class ForbiddenError(GalileoAPIError):
    """HTTP 403 - Insufficient permissions."""

    def __init__(self, status_code: int, content: bytes):
        super().__init__(
            status_code,
            content,
            "Permission denied. Your API key doesn't have access to this resource. "
            "Check your organization and project permissions.",
        )


class NotFoundError(GalileoAPIError):
    r"""HTTP 404 - Resource not found.

    Parameters
    ----------
    status_code_or_message : int | str
        Either an HTTP status code (``int``, paired with ``content``) or a
        full message string (``str``, used on its own).
    content : bytes, optional
        Raw response body. Only valid alongside an ``int`` status code; on the
        message path it must be omitted.

    Notes
    -----
    Two construction paths are supported, exposed via ``@overload`` so type
    checkers see the right shape per call site:

    - ``NotFoundError(status_code, content)`` — built from an HTTP 404 response
      by the generated client. Uses the standard "Resource not found…" message.
    - ``NotFoundError(message)`` — built from an SDK-level lookup that has no
      HTTP response (e.g. resolving a project from env vars). The string is the
      full message; no ``content`` argument is accepted.

    The runtime constructor also enforces the contract. The following all raise
    ``TypeError`` instead of producing nonsensical state:

    - Mixing shapes: ``NotFoundError("msg", b"")`` / ``NotFoundError("msg", b"body")``
    - Passing ``None``: ``NotFoundError(None)``
    - Passing ``bool``: ``NotFoundError(True, b"x")`` (``bool`` is technically an
      ``int`` subclass but is rejected explicitly to avoid silent acceptance)

    Examples
    --------
    >>> NotFoundError(404, b"{\\"detail\\": ...}")  # HTTP response path
    >>> NotFoundError("Project \\"foo\\" not found.")  # SDK lookup path
    """

    @overload
    def __init__(self, message: str) -> None: ...
    @overload
    def __init__(self, status_code: int, content: bytes) -> None: ...

    def __init__(self, status_code_or_message: int | str, content: bytes = _UNSET) -> None:
        if isinstance(status_code_or_message, str):
            if content is not _UNSET:
                raise TypeError(
                    "NotFoundError(message) does not accept a content argument. "
                    "Use NotFoundError(status_code, content) for HTTP-style construction."
                )
            self.status_code = 404
            self.content = b""
            self.message = status_code_or_message
            Exception.__init__(self, status_code_or_message)
        # mypy narrows to ``int`` here from the ``int | str`` annotation, so the
        # ``not isinstance(..., bool)`` half looks redundant statically — but at
        # runtime ``bool`` is an ``int`` subclass, so this guard is real
        # protection against callers passing ``True``/``False`` accidentally.
        elif isinstance(status_code_or_message, int) and not isinstance(  # type: ignore[redundant-expr]
            status_code_or_message, bool
        ):
            super().__init__(
                status_code_or_message,
                b"" if content is _UNSET else content,
                "Resource not found. The requested project, dataset, or resource doesn't exist. "
                "Verify the ID or name is correct.",
            )
        else:
            raise TypeError(
                "NotFoundError requires either (status_code: int, content: bytes) "
                f"or (message: str); got {type(status_code_or_message).__name__}."
            )


class ConflictError(GalileoAPIError):
    """HTTP 409 - Resource conflict."""

    def __init__(self, status_code: int, content: bytes):
        super().__init__(
            status_code,
            content,
            "Resource conflict. A resource with this name or ID already exists, "
            "or the operation conflicts with the current state.",
        )


class RateLimitError(GalileoAPIError):
    """HTTP 429 - Rate limit exceeded."""

    def __init__(self, status_code: int, content: bytes):
        super().__init__(
            status_code,
            content,
            "Rate limit exceeded. Too many requests. Please wait before retrying. "
            "Consider adding delays between API calls.",
        )


class ServerError(GalileoAPIError):
    """HTTP 5xx - Server-side error."""

    def __init__(self, status_code: int, content: bytes):
        super().__init__(
            status_code,
            content,
            "Server error. The Galileo API encountered an internal error. "
            "Please try again later or contact support if the issue persists.",
        )
