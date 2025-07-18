from typing import Literal, cast

ColumnCategory = Literal["dataset", "dataset_metadata", "feedback", "metric", "standard", "user_metadata"]

COLUMN_CATEGORY_VALUES: set[ColumnCategory] = {
    "dataset",
    "dataset_metadata",
    "feedback",
    "metric",
    "standard",
    "user_metadata",
}


def check_column_category(value: str) -> ColumnCategory:
    if value in COLUMN_CATEGORY_VALUES:
        return cast(ColumnCategory, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {COLUMN_CATEGORY_VALUES!r}")
