from typing import Any


def gcd_recursive(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm with recursion."""
    if b == 0:
        return a
    return gcd_recursive(b, a % b)


def is_instance_of(obj: Any, class_obj: Any) -> bool:
    return type(obj) is type(class_obj())
