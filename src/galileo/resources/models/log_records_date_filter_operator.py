from typing import Literal, cast

LogRecordsDateFilterOperator = Literal["eq", "gt", "gte", "lt", "lte", "ne"]

LOG_RECORDS_DATE_FILTER_OPERATOR_VALUES: set[LogRecordsDateFilterOperator] = {"eq", "gt", "gte", "lt", "lte", "ne"}


def check_log_records_date_filter_operator(value: str) -> LogRecordsDateFilterOperator:
    if value in LOG_RECORDS_DATE_FILTER_OPERATOR_VALUES:
        return cast(LogRecordsDateFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_RECORDS_DATE_FILTER_OPERATOR_VALUES!r}")
