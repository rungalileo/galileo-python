from typing import Literal, cast

TaskType = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

TASK_TYPE_VALUES: set[TaskType] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17}


def check_task_type(value: int) -> TaskType:
    if value in TASK_TYPE_VALUES:
        return cast(TaskType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TASK_TYPE_VALUES!r}")
