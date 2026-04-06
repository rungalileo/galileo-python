"""Deprecated: use galileo.shared.column instead of galileo.__future__.shared.column."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.shared.column is deprecated. Use galileo.shared.column instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.shared.column import Column, ColumnCollection, _unwrap_unset  # noqa: E402

__all__ = ["Column", "ColumnCollection", "_unwrap_unset"]
