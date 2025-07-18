from typing import Literal, cast

LogRecordsTextFilterOperator = Literal["contains", "eq", "ne", "not_in", "one_of"]

LOG_RECORDS_TEXT_FILTER_OPERATOR_VALUES: set[LogRecordsTextFilterOperator] = {
    "contains",
    "eq",
    "ne",
    "not_in",
    "one_of",
}


def check_log_records_text_filter_operator(value: str) -> LogRecordsTextFilterOperator:
    if value in LOG_RECORDS_TEXT_FILTER_OPERATOR_VALUES:
        return cast(LogRecordsTextFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_RECORDS_TEXT_FILTER_OPERATOR_VALUES!r}")
