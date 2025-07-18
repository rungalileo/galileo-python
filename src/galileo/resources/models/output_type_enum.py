from typing import Literal, cast

OutputTypeEnum = Literal["boolean", "categorical", "count", "discrete", "freeform", "percentage"]

OUTPUT_TYPE_ENUM_VALUES: set[OutputTypeEnum] = {"boolean", "categorical", "count", "discrete", "freeform", "percentage"}


def check_output_type_enum(value: str) -> OutputTypeEnum:
    if value in OUTPUT_TYPE_ENUM_VALUES:
        return cast(OutputTypeEnum, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {OUTPUT_TYPE_ENUM_VALUES!r}")
