from typing import Literal, cast

DatasetFormat = Literal["csv", "feather", "json", "jsonl"]

DATASET_FORMAT_VALUES: set[DatasetFormat] = {"csv", "feather", "json", "jsonl"}


def check_dataset_format(value: str) -> DatasetFormat:
    if value in DATASET_FORMAT_VALUES:
        return cast(DatasetFormat, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATASET_FORMAT_VALUES!r}")
