"""Deprecated: use galileo.types instead of galileo.__future__.types."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.types is deprecated. Use galileo.types instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.types import MetricSpec  # noqa: E402

__all__ = ["MetricSpec"]
