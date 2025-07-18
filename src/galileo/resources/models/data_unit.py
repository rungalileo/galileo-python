from typing import Literal, cast

DataUnit = Literal["count_and_total", "dollars", "milli_seconds", "nano_seconds", "percentage"]

DATA_UNIT_VALUES: set[DataUnit] = {"count_and_total", "dollars", "milli_seconds", "nano_seconds", "percentage"}


def check_data_unit(value: str) -> DataUnit:
    if value in DATA_UNIT_VALUES:
        return cast(DataUnit, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATA_UNIT_VALUES!r}")
