from functools import wraps
from typing import Any, Callable, TypeVar

from galileo.__future__.shared.exceptions import ValidationError

R = TypeVar("R")


def require_exactly_one(*param_names: str) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """
    Decorator to ensure that exactly one of the given keyword arguments is provided (not None).

    Raises
    ------
        ValidationError: If neither or both parameters are provided.

    Examples
    --------
    ```python
    @require_exactly_one("project_id", "project_name")
    def list(*, project_id=None, project_name=None):
        ...
    ```
    """

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            provided = [name for name in param_names if kwargs.get(name) is not None]

            if len(provided) == 0:
                raise ValidationError(
                    f"{func.__name__}() requires exactly one of {', '.join(param_names)}, but neither was defined."
                )
            if len(provided) == 2:
                raise ValidationError(
                    f"{func.__name__}() requires exactly one of {', '.join(param_names)}, but both were defined."
                )
            if len(provided) > 2:
                raise ValidationError(
                    f"{func.__name__}() requires exactly one of {', '.join(param_names)}, but many were defined: {', '.join(provided)}."
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
