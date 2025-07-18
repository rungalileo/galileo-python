from typing import Literal, cast

ProjectNameFilterOperator = Literal["contains", "eq", "ne", "not_in", "one_of"]

PROJECT_NAME_FILTER_OPERATOR_VALUES: set[ProjectNameFilterOperator] = {"contains", "eq", "ne", "not_in", "one_of"}


def check_project_name_filter_operator(value: str) -> ProjectNameFilterOperator:
    if value in PROJECT_NAME_FILTER_OPERATOR_VALUES:
        return cast(ProjectNameFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_NAME_FILTER_OPERATOR_VALUES!r}")
