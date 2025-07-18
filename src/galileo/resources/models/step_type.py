from typing import Literal, cast

StepType = Literal["agent", "llm", "retriever", "session", "tool", "trace", "workflow"]

STEP_TYPE_VALUES: set[StepType] = {"agent", "llm", "retriever", "session", "tool", "trace", "workflow"}


def check_step_type(value: str) -> StepType:
    if value in STEP_TYPE_VALUES:
        return cast(StepType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {STEP_TYPE_VALUES!r}")
