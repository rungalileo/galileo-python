from typing import Literal, cast

ProjectUpdatedAtFilterOperator = Literal["eq", "gt", "gte", "lt", "lte", "ne"]

PROJECT_UPDATED_AT_FILTER_OPERATOR_VALUES: set[ProjectUpdatedAtFilterOperator] = {"eq", "gt", "gte", "lt", "lte", "ne"}


def check_project_updated_at_filter_operator(value: str) -> ProjectUpdatedAtFilterOperator:
    if value in PROJECT_UPDATED_AT_FILTER_OPERATOR_VALUES:
        return cast(ProjectUpdatedAtFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_UPDATED_AT_FILTER_OPERATOR_VALUES!r}")
