"""
Unified type definitions for the Galileo Future API.

This module provides type aliases that reduce friction when working with metrics
and other Galileo objects.
"""

from typing import Union

from galileo.__future__.metric import Metric
from galileo.schema.metrics import GalileoMetricNames, GalileoMetrics, LocalMetricConfig

# Unified metric type that accepts all valid metric specifications
MetricSpec = Union[
    GalileoMetrics,  # Built-in scorer enum (deprecated — internal names like "correctness")
    GalileoMetricNames,  # Human-readable labels (preferred — e.g., "Context Adherence")
    Metric,  # Custom or local metric object
    LocalMetricConfig,  # Legacy local metric config
    str,  # String name, label, or UUID of a metric
]

__all__ = ["MetricSpec"]
