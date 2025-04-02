import functools
import logging
import os
from typing import Any, Callable

_logger = logging.getLogger(__name__)


def galileo_logging_enabled() -> bool:
    if os.getenv("GALILEO_LOGGING_DISABLED", "false").lower() in ("true", "1", "t"):
        return False
    return True


def nop_sync(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        if galileo_logging_enabled():
            return f(*args, **kwargs)
        _logger.warning(f"Bypassing logging for {f.__name__}. Logging is currently disabled.")

    return decorated


def nop_async(f: Callable) -> Callable:
    @functools.wraps(f)
    async def decorated(*args: Any, **kwargs: Any) -> Any:
        if galileo_logging_enabled():
            return await f(*args, **kwargs)
        _logger.warning(f"Bypassing logging for {f.__name__}. Logging is currently disabled.")

    return decorated
