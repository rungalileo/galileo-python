from typing import Literal, cast

InsightType = Literal["horizontal_bar", "vertical_bar"]

INSIGHT_TYPE_VALUES: set[InsightType] = {"horizontal_bar", "vertical_bar"}


def check_insight_type(value: str) -> InsightType:
    if value in INSIGHT_TYPE_VALUES:
        return cast(InsightType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INSIGHT_TYPE_VALUES!r}")
