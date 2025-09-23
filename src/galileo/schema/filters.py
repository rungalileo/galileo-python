from typing import Union

from galileo.resources.models import (
    LogRecordsBooleanFilter,
    LogRecordsDateFilter,
    LogRecordsIDFilter,
    LogRecordsNumberFilter,
    LogRecordsTextFilter,
)

FilterType = Union[
    LogRecordsBooleanFilter, LogRecordsDateFilter, LogRecordsIDFilter, LogRecordsNumberFilter, LogRecordsTextFilter
]
