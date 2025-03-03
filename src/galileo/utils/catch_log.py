import functools
import logging
from logging import Logger
from typing import Any


def warn_catch_exception(logger: Logger = logging.getLogger(__name__), exception: BaseException = Exception) -> Any:
    """
    A function wrapper that catches exceptions and logs them to the logger.
    Args:
        exception:
        logger:

    Returns:

    """

    def wrapper(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
            except exception as err:
                logger.warning(f"error happend during executing {f.__name__}: {err}")
            else:
                return result

        return inner

    return wrapper


class DecorateAllMethods:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for attr, f in cls.__dict__.items():
            if callable(f):
                setattr(cls, attr, warn_catch_exception()(f))
