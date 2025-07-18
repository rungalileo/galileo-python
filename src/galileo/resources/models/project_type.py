from typing import Literal, cast

ProjectType = Literal["gen_ai", "llm_monitor", "prompt_evaluation", "protect", "training_inference"]

PROJECT_TYPE_VALUES: set[ProjectType] = {"gen_ai", "llm_monitor", "prompt_evaluation", "protect", "training_inference"}


def check_project_type(value: str) -> ProjectType:
    if value in PROJECT_TYPE_VALUES:
        return cast(ProjectType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_TYPE_VALUES!r}")
