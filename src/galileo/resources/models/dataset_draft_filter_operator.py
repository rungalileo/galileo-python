from typing import Literal, cast

DatasetDraftFilterOperator = Literal["eq", "ne"]

DATASET_DRAFT_FILTER_OPERATOR_VALUES: set[DatasetDraftFilterOperator] = {"eq", "ne"}


def check_dataset_draft_filter_operator(value: str) -> DatasetDraftFilterOperator:
    if value in DATASET_DRAFT_FILTER_OPERATOR_VALUES:
        return cast(DatasetDraftFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATASET_DRAFT_FILTER_OPERATOR_VALUES!r}")
