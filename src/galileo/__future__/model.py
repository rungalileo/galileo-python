"""Deprecated: use galileo.model instead of galileo.__future__.model."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.model is deprecated. Use galileo.model instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.model import Model  # noqa: E402

__all__ = ["Model"]
