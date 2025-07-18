from typing import Literal, cast

DatasetAction = Literal["delete", "export", "rename", "share", "update"]

DATASET_ACTION_VALUES: set[DatasetAction] = {"delete", "export", "rename", "share", "update"}


def check_dataset_action(value: str) -> DatasetAction:
    if value in DATASET_ACTION_VALUES:
        return cast(DatasetAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATASET_ACTION_VALUES!r}")
