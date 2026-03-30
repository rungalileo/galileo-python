"""Deprecated: use galileo.project instead of galileo.__future__.project."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.project is deprecated. Use galileo.project instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.project import Project  # noqa: E402

__all__ = ["Project"]
