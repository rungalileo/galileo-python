from enum import Enum


class AlertConditionType(str, Enum):
    METRICARRAY_STRING1 = "metric/array_string/1"
    METRICNUMERIC1 = "metric/numeric/1"
    METRICSTRING1 = "metric/string/1"
    ROOTNUMERIC1 = "root/numeric/1"

    def __str__(self) -> str:
        return str(self.value)
