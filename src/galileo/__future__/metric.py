"""Deprecated: use galileo.metric instead of galileo.__future__.metric."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.metric is deprecated. Use galileo.metric instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.metric import BuiltInMetrics, CodeMetric, GalileoMetric, LlmMetric, LocalMetric, Metric  # noqa: E402

__all__ = ["BuiltInMetrics", "CodeMetric", "GalileoMetric", "LlmMetric", "LocalMetric", "Metric"]
