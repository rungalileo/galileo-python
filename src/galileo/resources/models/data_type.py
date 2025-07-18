from typing import Literal, cast

DataType = Literal["boolean", "floating_point", "integer", "string_list", "text", "timestamp", "uuid"]

DATA_TYPE_VALUES: set[DataType] = {"boolean", "floating_point", "integer", "string_list", "text", "timestamp", "uuid"}


def check_data_type(value: str) -> DataType:
    if value in DATA_TYPE_VALUES:
        return cast(DataType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATA_TYPE_VALUES!r}")
