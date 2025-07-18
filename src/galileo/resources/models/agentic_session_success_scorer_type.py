from typing import Literal, cast

AgenticSessionSuccessScorerType = Literal["luna", "plus"]

AGENTIC_SESSION_SUCCESS_SCORER_TYPE_VALUES: set[AgenticSessionSuccessScorerType] = {"luna", "plus"}


def check_agentic_session_success_scorer_type(value: str) -> AgenticSessionSuccessScorerType:
    if value in AGENTIC_SESSION_SUCCESS_SCORER_TYPE_VALUES:
        return cast(AgenticSessionSuccessScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AGENTIC_SESSION_SUCCESS_SCORER_TYPE_VALUES!r}")
