from galileo.resources.models import (
    LogRecordsBooleanFilter,
    LogRecordsDateFilter,
    LogRecordsIDFilter,
    LogRecordsNumberFilter,
    LogRecordsTextFilter,
)

FilterType = (
    LogRecordsBooleanFilter | LogRecordsDateFilter | LogRecordsIDFilter | LogRecordsNumberFilter | LogRecordsTextFilter
)
