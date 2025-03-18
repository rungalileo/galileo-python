import asyncio
import functools
import logging
from logging import Logger
from typing import Any, Callable


def warn_catch_exception(logger: Logger = logging.getLogger(__name__), exception: type[Exception] = Exception) -> Any:
    """
    A function wrapper that catches exceptions and logs them to the logger.
    Args:
        exception:
        logger:

    Returns:

    """

    def wrapper(f: Callable) -> Callable:
        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                result = f(*args, **kwargs)
            except exception as err:
                logger.warning(f"Error occurred during execution: {f.__name__}: {err}")
            else:
                return result

        return inner

    return wrapper


def async_warn_catch_exception(
    logger: Logger = logging.getLogger(__name__), exception: type[Exception] = Exception
) -> Any:
    """
    A function wrapper that catches exceptions and logs them to the logger.
    Args:
        exception:
        logger:

    Returns:

    """

    def wrapper(f: Callable) -> Callable:
        @functools.wraps(f)
        async def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                result = await f(*args, **kwargs)
            except exception as err:
                logger.warning(f"Error occurred during execution: {f.__name__}: {err}")
            else:
                return result

        return inner

    return wrapper


class DecorateAllMethods:
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        for attr, f in cls.__dict__.items():
            if attr == "__init__":
                continue
            if callable(f):
                if asyncio.iscoroutinefunction(f):
                    setattr(cls, attr, async_warn_catch_exception()(f))
                else:
                    setattr(cls, attr, warn_catch_exception()(f))
