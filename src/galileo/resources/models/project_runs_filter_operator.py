from typing import Literal, cast

ProjectRunsFilterOperator = Literal["between", "eq", "gt", "gte", "lt", "lte", "ne"]

PROJECT_RUNS_FILTER_OPERATOR_VALUES: set[ProjectRunsFilterOperator] = {"between", "eq", "gt", "gte", "lt", "lte", "ne"}


def check_project_runs_filter_operator(value: str) -> ProjectRunsFilterOperator:
    if value in PROJECT_RUNS_FILTER_OPERATOR_VALUES:
        return cast(ProjectRunsFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_RUNS_FILTER_OPERATOR_VALUES!r}")
