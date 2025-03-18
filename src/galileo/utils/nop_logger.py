import asyncio
import functools
import logging
import os
from typing import Any, Callable

_logger = logging.getLogger(__name__)


def galileo_logging_enabled() -> bool:
    if os.getenv("GALILEO_LOGGING_DISABLED", "False").lower() in ("true", "1", "t"):
        return True
    return False


def nop_sync(*args, **kwargs) -> Any:
    def wrapper(f: Callable) -> Callable:
        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            _logger.debug(f"enabled nop logger for {f.__name__}")

        return inner

    return wrapper


def nop_async(*args: Any, **kwargs: Any) -> Any:
    def wrapper(f: Callable) -> Callable:
        @functools.wraps(f)
        async def inner(*args: Any, **kwargs: Any) -> Any:
            _logger.debug(f"enabled nop logger for {f.__name__}")

        return inner

    return wrapper


class NopAllMethods:
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        if galileo_logging_enabled():
            for attr, f in cls.__dict__.items():
                if callable(f):
                    if asyncio.iscoroutinefunction(f):
                        setattr(cls, attr, nop_async()(f))
                    else:
                        setattr(cls, attr, nop_sync()(f))
