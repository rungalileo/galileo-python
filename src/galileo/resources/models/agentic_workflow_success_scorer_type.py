from typing import Literal, cast

AgenticWorkflowSuccessScorerType = Literal["luna", "plus"]

AGENTIC_WORKFLOW_SUCCESS_SCORER_TYPE_VALUES: set[AgenticWorkflowSuccessScorerType] = {"luna", "plus"}


def check_agentic_workflow_success_scorer_type(value: str) -> AgenticWorkflowSuccessScorerType:
    if value in AGENTIC_WORKFLOW_SUCCESS_SCORER_TYPE_VALUES:
        return cast(AgenticWorkflowSuccessScorerType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AGENTIC_WORKFLOW_SUCCESS_SCORER_TYPE_VALUES!r}")
