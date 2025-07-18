from typing import Literal, cast

ToolErrorRateScorerType = Literal["luna", "plus"]

TOOL_ERROR_RATE_SCORER_TYPE_VALUES: set[ToolErrorRateScorerType] = {"luna", "plus"}


def check_tool_error_rate_scorer_type(value: str) -> ToolErrorRateScorerType:
    if value in TOOL_ERROR_RATE_SCORER_TYPE_VALUES:
        return cast(ToolErrorRateScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TOOL_ERROR_RATE_SCORER_TYPE_VALUES!r}")
