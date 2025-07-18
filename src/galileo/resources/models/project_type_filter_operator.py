from typing import Literal, cast

ProjectTypeFilterOperator = Literal["eq", "ne", "not_in", "one_of"]

PROJECT_TYPE_FILTER_OPERATOR_VALUES: set[ProjectTypeFilterOperator] = {"eq", "ne", "not_in", "one_of"}


def check_project_type_filter_operator(value: str) -> ProjectTypeFilterOperator:
    if value in PROJECT_TYPE_FILTER_OPERATOR_VALUES:
        return cast(ProjectTypeFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_TYPE_FILTER_OPERATOR_VALUES!r}")
