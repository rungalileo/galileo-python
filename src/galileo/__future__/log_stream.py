"""Deprecated: use galileo.log_stream instead of galileo.__future__.log_stream."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.log_stream is deprecated. Use galileo.log_stream instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.log_stream import LogStream  # noqa: E402

__all__ = ["LogStream"]
