"""Deprecated: use galileo.shared.base instead of galileo.__future__.shared.base."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.shared.base is deprecated. Use galileo.shared.base instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.shared.base import StateManagementMixin, SyncState  # noqa: E402

__all__ = ["StateManagementMixin", "SyncState"]
