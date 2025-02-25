from importlib.util import find_spec


def is_dependency_available(name: str) -> bool:
    return find_spec(name) is not None


is_langchain_available = is_dependency_available("langchain_core")
