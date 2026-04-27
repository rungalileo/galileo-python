from enum import Enum


class WidgetType(str, Enum):
    BAR_CHART = "bar_chart"
    LINE_CHART = "line_chart"
    NUMBER = "number"
    TABLE = "table"

    def __str__(self) -> str:
        return str(self.value)
