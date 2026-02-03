"""
Decorators for resilient ingestion/telemetry operations.

These decorators should ONLY be used for fire-and-forget operations where failures
should not crash the user's application (e.g., trace ingestion, span logging).

DO NOT use for resource management operations (CRUD) - those should raise exceptions
so users get clear feedback about failures.
"""

import functools
import logging
from logging import Logger
from typing import Any, Callable

import httpx

from galileo_core.exceptions.http import GalileoHTTPException

# Infrastructure exceptions that should be swallowed for ingestion operations.
# These are network-level errors that are outside the user's control.
INFRASTRUCTURE_EXCEPTIONS: tuple[type[Exception], ...] = (
    httpx.HTTPError,
    httpx.TimeoutException,
    httpx.ConnectError,
    httpx.ReadError,
    httpx.WriteError,
    ConnectionError,
    TimeoutError,
    OSError,
)


def warn_catch_exception(
    logger: Logger = logging.getLogger(__name__), exceptions: tuple[type[Exception], ...] = INFRASTRUCTURE_EXCEPTIONS
) -> Callable:
    """
    Decorator for resilient synchronous ingestion/telemetry operations.

    Catches infrastructure exceptions (network errors, timeouts) and logs them
    as warnings instead of raising. Returns None when an exception is caught.

    Use this decorator ONLY for fire-and-forget operations where failures
    should not crash the user's application (e.g., trace ingestion).

    DO NOT use for resource management operations (CRUD) - those should raise.

    Parameters
    ----------
    logger : Logger
        The logger to use for warning messages. Defaults to module logger.
    exceptions : tuple[type[Exception], ...]
        Tuple of exception types to catch. Defaults to INFRASTRUCTURE_EXCEPTIONS.

    Returns
    -------
    Callable
        A decorator that wraps the function with exception handling.

    Examples
    --------
    ```python
    @warn_catch_exception()
    def ingest_trace(trace_data: dict) -> None:
        # Network errors will be caught and logged, not raised
        api_client.post("/traces", json=trace_data)
    ```
    """

    def wrapper(f: Callable) -> Callable:
        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                return f(*args, **kwargs)
            except exceptions as err:
                logger.warning(f"Ingestion error in {f.__name__}: {err}")
                return None

        return inner

    return wrapper


def async_warn_catch_exception(
    logger: Logger = logging.getLogger(__name__), exceptions: tuple[type[Exception], ...] = INFRASTRUCTURE_EXCEPTIONS
) -> Callable:
    """
    Decorator for resilient asynchronous ingestion/telemetry operations.

    Catches infrastructure exceptions (network errors, timeouts) and logs them
    as warnings instead of raising. Returns None when an exception is caught.

    Use this decorator ONLY for fire-and-forget operations where failures
    should not crash the user's application (e.g., async trace ingestion).

    DO NOT use for resource management operations (CRUD) - those should raise.

    Parameters
    ----------
    logger : Logger
        The logger to use for warning messages. Defaults to module logger.
    exceptions : tuple[type[Exception], ...]
        Tuple of exception types to catch. Defaults to INFRASTRUCTURE_EXCEPTIONS.

    Returns
    -------
    Callable
        A decorator that wraps the async function with exception handling.

    Examples
    --------
    ```python
    @async_warn_catch_exception()
    async def ingest_trace(trace_data: dict) -> None:
        # Network errors will be caught and logged, not raised
        await api_client.post("/traces", json=trace_data)
    ```
    """

    def wrapper(f: Callable) -> Callable:
        @functools.wraps(f)
        async def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                return await f(*args, **kwargs)
            except exceptions as err:
                logger.warning(f"Ingestion error in {f.__name__}: {err}")
                return None

        return inner

    return wrapper


# HTTP status codes that indicate transient errors worth retrying
RETRYABLE_STATUS_CODES: frozenset[int] = frozenset(
    {
        404,  # Not found - record may not be ingested yet (eventual consistency)
        408,  # Request timeout
        422,  # Unprocessable entity - parent record may not exist yet
        429,  # Rate limited
    }
)

_retry_logger = logging.getLogger(__name__)


def retry_on_transient_http_error(func: Callable) -> Callable:
    """
    Decorator for backoff retry logic on transient HTTP errors.

    This decorator is designed to work WITH the backoff library. It catches
    GalileoHTTPException and decides whether to re-raise (triggering a retry)
    or return None (giving up silently).

    Retryable errors (re-raised for backoff):
    - 404: Record not found (eventual consistency)
    - 408: Request timeout
    - 422: Parent record not found yet
    - 429: Rate limited
    - 500+: Server errors

    Non-retryable errors (returns None, logs error):
    - 401: Unauthorized
    - 403: Forbidden
    - 400: Bad request
    - Other client errors

    Parameters
    ----------
    func : Callable
        An async function to wrap with retry logic.

    Returns
    -------
    Callable
        The wrapped async function.

    Examples
    --------
    ```python
    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    @retry_on_transient_http_error
    async def update_trace(request: TraceUpdateRequest) -> None:
        await api_client.update_trace(request)
    ```

    Note
    ----
    This decorator only works with async functions. It's designed to be used
    as the innermost decorator, with backoff as the outer decorator.
    """

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except GalileoHTTPException as e:
            if e.status_code in RETRYABLE_STATUS_CODES:
                _retry_logger.info("HTTP %d error, retrying...", e.status_code)
                raise
            if e.status_code >= 500:
                _retry_logger.info("Server error (HTTP %d), retrying...", e.status_code)
                raise

            _retry_logger.error("Unrecoverable HTTP error (status %d): %s", e.status_code, e)
            return None

    return wrapper
