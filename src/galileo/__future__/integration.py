"""Deprecated: use galileo.integration instead of galileo.__future__.integration."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.integration is deprecated. Use galileo.integration instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.integration import Integration  # noqa: E402

__all__ = ["Integration"]
