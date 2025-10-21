"""
Unified type definitions for the Galileo Future API.

This module provides type aliases that reduce friction when working with metrics
and other Galileo objects.
"""

from typing import Union

from galileo.__future__.metric import Metric
from galileo.schema.metrics import GalileoScorers, LocalMetricConfig

# Unified metric type that accepts all valid metric specifications
MetricSpec = Union[
    GalileoScorers,      # Built-in scorer enum (e.g., GalileoScorers.correctness)
    Metric,              # Custom or local metric object
    LocalMetricConfig,   # Legacy local metric config
    str,                 # String name of built-in metric (e.g., "correctness")
]

__all__ = ["MetricSpec"]

