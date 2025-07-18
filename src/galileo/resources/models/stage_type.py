from typing import Literal, cast

StageType = Literal["central", "local"]

STAGE_TYPE_VALUES: set[StageType] = {"central", "local"}


def check_stage_type(value: str) -> StageType:
    if value in STAGE_TYPE_VALUES:
        return cast(StageType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {STAGE_TYPE_VALUES!r}")
