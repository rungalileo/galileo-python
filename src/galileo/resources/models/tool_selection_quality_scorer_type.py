from typing import Literal, cast

ToolSelectionQualityScorerType = Literal["luna", "plus"]

TOOL_SELECTION_QUALITY_SCORER_TYPE_VALUES: set[ToolSelectionQualityScorerType] = {"luna", "plus"}


def check_tool_selection_quality_scorer_type(value: str) -> ToolSelectionQualityScorerType:
    if value in TOOL_SELECTION_QUALITY_SCORER_TYPE_VALUES:
        return cast(ToolSelectionQualityScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TOOL_SELECTION_QUALITY_SCORER_TYPE_VALUES!r}")
