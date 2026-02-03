"""
Decorators for conditionally enabling/disabling Galileo telemetry.

These decorators check the GALILEO_LOGGING_DISABLED environment variable
and skip execution of telemetry operations when disabled.
"""

import functools
import logging
import os
from typing import Any, Callable

_logger = logging.getLogger(__name__)


def galileo_logging_enabled() -> bool:
    """
    Check if Galileo logging/telemetry is enabled.

    Returns
    -------
    bool
        True if logging is enabled (default), False if GALILEO_LOGGING_DISABLED is set.
    """
    return os.getenv("GALILEO_LOGGING_DISABLED", "false").lower() not in ("true", "1", "t")


def nop_sync(f: Callable) -> Callable:
    """
    Decorator that skips execution of sync functions when Galileo logging is disabled.

    When GALILEO_LOGGING_DISABLED is set to "true", "1", or "t", the decorated
    function will not execute and will return None instead.

    Parameters
    ----------
    f : Callable
        The synchronous function to wrap.

    Returns
    -------
    Callable
        A wrapped function that checks the logging toggle before execution.
    """

    @functools.wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        if galileo_logging_enabled():
            return f(*args, **kwargs)
        _logger.debug(f"Bypassing logging for {f.__name__}. Logging is currently disabled.")
        return None

    return decorated


def nop_async(f: Callable) -> Callable:
    """
    Decorator that skips execution of async functions when Galileo logging is disabled.

    When GALILEO_LOGGING_DISABLED is set to "true", "1", or "t", the decorated
    function will not execute and will return None instead.

    Parameters
    ----------
    f : Callable
        The asynchronous function to wrap.

    Returns
    -------
    Callable
        A wrapped async function that checks the logging toggle before execution.
    """

    @functools.wraps(f)
    async def decorated(*args: Any, **kwargs: Any) -> Any:
        if galileo_logging_enabled():
            return await f(*args, **kwargs)
        _logger.debug(f"Bypassing logging for {f.__name__}. Logging is currently disabled.")
        return None

    return decorated
