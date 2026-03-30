"""Deprecated: use galileo.shared.utils instead of galileo.__future__.shared.utils."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.shared.utils is deprecated. Use galileo.shared.utils instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.shared.utils import classproperty  # noqa: E402

__all__ = ["classproperty"]
