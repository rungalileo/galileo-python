from typing import Literal, cast

DatasetContentFilterOperator = Literal["contains", "eq", "ne"]

DATASET_CONTENT_FILTER_OPERATOR_VALUES: set[DatasetContentFilterOperator] = {"contains", "eq", "ne"}


def check_dataset_content_filter_operator(value: str) -> DatasetContentFilterOperator:
    if value in DATASET_CONTENT_FILTER_OPERATOR_VALUES:
        return cast(DatasetContentFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATASET_CONTENT_FILTER_OPERATOR_VALUES!r}")
