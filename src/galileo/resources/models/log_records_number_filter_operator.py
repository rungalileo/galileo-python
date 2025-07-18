from typing import Literal, cast

LogRecordsNumberFilterOperator = Literal["between", "eq", "gt", "gte", "lt", "lte", "ne"]

LOG_RECORDS_NUMBER_FILTER_OPERATOR_VALUES: set[LogRecordsNumberFilterOperator] = {
    "between",
    "eq",
    "gt",
    "gte",
    "lt",
    "lte",
    "ne",
}


def check_log_records_number_filter_operator(value: str) -> LogRecordsNumberFilterOperator:
    if value in LOG_RECORDS_NUMBER_FILTER_OPERATOR_VALUES:
        return cast(LogRecordsNumberFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_RECORDS_NUMBER_FILTER_OPERATOR_VALUES!r}")
