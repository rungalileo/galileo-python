"""Galileo SDK exceptions."""


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
            "Set via GALILEO_API_KEY environment variable or galileo.configure(api_key=...).",
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
    """HTTP 404 - Resource not found."""

    def __init__(self, status_code: int, content: bytes):
        super().__init__(
            status_code,
            content,
            "Resource not found. The requested project, dataset, or resource doesn't exist. "
            "Verify the ID or name is correct.",
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
