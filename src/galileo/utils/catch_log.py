import asyncio
import functools
import logging
import warnings
from logging import Logger
from typing import Any, Callable


def warn_catch_exception(logger: Logger = logging.getLogger(__name__), exception: type[Exception] = Exception) -> Any:
    """
    A function wrapper that catches exceptions, logs them, and emits visible warnings.

    This decorator ensures that observability code doesn't crash the user's application
    while still providing visible feedback when errors occur.

    Errors are:
    1. Logged via standard Python logging (integrates with logging/tracing platforms)
    2. Emitted as warnings (visible by default without any logging configuration)

    Parameters
    ----------
    exception : type[Exception]
        The base exception type to catch. Defaults to Exception.

    Returns
    -------
    Callable
        The decorated function.
    """

    def wrapper(f: Callable) -> Callable:
        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                result = f(*args, **kwargs)
            except exception as err:
                # Standard logging for integration with logging/tracing platforms
                logger.warning(f"Error occurred during execution: {f.__name__}: {err}")
                # Warning for immediate visibility without config
                warnings.warn(f"Galileo: {f.__name__} failed: {err}", RuntimeWarning, stacklevel=2)
            else:
                return result

        return inner

    return wrapper


def async_warn_catch_exception(
    logger: Logger = logging.getLogger(__name__), exception: type[Exception] = Exception
) -> Any:
    """
    An async function wrapper that catches exceptions, logs them, and emits visible warnings.

    This decorator ensures that observability code doesn't crash the user's application
    while still providing visible feedback when errors occur.

    Errors are:
    1. Logged via standard Python logging (integrates with logging/tracing platforms)
    2. Emitted as warnings (visible by default without any logging configuration)

    Parameters
    ----------
    logger : Logger
        The logger to use for logging errors. Defaults to the module logger.
    exception : type[Exception]
        The base exception type to catch. Defaults to Exception.

    Returns
    -------
    Callable
        The decorated function.
    """

    def wrapper(f: Callable) -> Callable:
        @functools.wraps(f)
        async def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                result = await f(*args, **kwargs)
            except exception as err:
                # Standard logging for integration with logging/tracing platforms
                logger.warning(f"Error occurred during execution: {f.__name__}: {err}")
                # Warning for immediate visibility without config
                warnings.warn(f"Galileo: {f.__name__} failed: {err}", RuntimeWarning, stacklevel=2)
            else:
                return result

        return inner

    return wrapper


class DecorateAllMethods:
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Methods to exclude from decoration (should raise exceptions)
        excluded_methods = {"__init__", "get_tracing_headers"}
        for attr, f in cls.__dict__.items():
            if attr in excluded_methods:
                continue
            if callable(f):
                if asyncio.iscoroutinefunction(f):
                    setattr(cls, attr, async_warn_catch_exception()(f))
                else:
                    setattr(cls, attr, warn_catch_exception()(f))
