from typing import Literal, cast

MetricComputationStatus = Literal["error", "failed", "success", "timeout"]

METRIC_COMPUTATION_STATUS_VALUES: set[MetricComputationStatus] = {"error", "failed", "success", "timeout"}


def check_metric_computation_status(value: str) -> MetricComputationStatus:
    if value in METRIC_COMPUTATION_STATUS_VALUES:
        return cast(MetricComputationStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {METRIC_COMPUTATION_STATUS_VALUES!r}")
