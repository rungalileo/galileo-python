from typing import Literal, cast

ProjectCreatedAtFilterOperator = Literal["eq", "gt", "gte", "lt", "lte", "ne"]

PROJECT_CREATED_AT_FILTER_OPERATOR_VALUES: set[ProjectCreatedAtFilterOperator] = {"eq", "gt", "gte", "lt", "lte", "ne"}


def check_project_created_at_filter_operator(value: str) -> ProjectCreatedAtFilterOperator:
    if value in PROJECT_CREATED_AT_FILTER_OPERATOR_VALUES:
        return cast(ProjectCreatedAtFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CREATED_AT_FILTER_OPERATOR_VALUES!r}")
