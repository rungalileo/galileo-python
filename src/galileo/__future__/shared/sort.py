"""Deprecated: use galileo.shared.sort instead of galileo.__future__.shared.sort."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.shared.sort is deprecated. Use galileo.shared.sort instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.shared.sort import Sort, sort  # noqa: E402

__all__ = ["Sort", "sort"]
