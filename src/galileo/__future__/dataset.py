"""Deprecated: use galileo.dataset instead of galileo.__future__.dataset."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.dataset is deprecated. Use galileo.dataset instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.dataset import Dataset  # noqa: E402

__all__ = ["Dataset"]
