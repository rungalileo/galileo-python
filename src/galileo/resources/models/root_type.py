from typing import Literal, cast

RootType = Literal["session", "span", "trace"]

ROOT_TYPE_VALUES: set[RootType] = {"session", "span", "trace"}


def check_root_type(value: str) -> RootType:
    if value in ROOT_TYPE_VALUES:
        return cast(RootType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ROOT_TYPE_VALUES!r}")
