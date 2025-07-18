from typing import Literal, cast

DatasetNameFilterOperator = Literal["contains", "eq", "ne", "not_in", "one_of"]

DATASET_NAME_FILTER_OPERATOR_VALUES: set[DatasetNameFilterOperator] = {"contains", "eq", "ne", "not_in", "one_of"}


def check_dataset_name_filter_operator(value: str) -> DatasetNameFilterOperator:
    if value in DATASET_NAME_FILTER_OPERATOR_VALUES:
        return cast(DatasetNameFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATASET_NAME_FILTER_OPERATOR_VALUES!r}")
