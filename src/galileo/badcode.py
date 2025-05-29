from typing import Any


def gcd_recursive(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm with recursion."""
    # Optimized: Iterative version to eliminate Python function call overhead.
    while b != 0:
        a, b = b, a % b
    return a


def is_instance_of(obj: Any, class_obj: Any) -> bool:
    return type(obj) is type(class_obj())
