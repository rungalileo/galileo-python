from typing import Literal, cast

ProjectLabels = Literal["sample"]

PROJECT_LABELS_VALUES: set[ProjectLabels] = {"sample"}


def check_project_labels(value: str) -> ProjectLabels:
    if value in PROJECT_LABELS_VALUES:
        return cast(ProjectLabels, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_LABELS_VALUES!r}")
