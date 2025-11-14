from typing import Any, Callable


class classproperty:
    """Decorator for class-level properties."""

    def __init__(self, func: Callable[[Any], Any]) -> None:
        self.func = func
        self.__doc__ = func.__doc__

    def __get__(self, obj: Any, owner: Any) -> Any:
        return self.func(owner)

    def __set__(self, obj: Any, value: Any) -> None:
        raise AttributeError("can't set attribute")
