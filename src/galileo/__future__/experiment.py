"""Deprecated: use galileo.experiment instead of galileo.__future__.experiment."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.experiment is deprecated. Use galileo.experiment instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.experiment import Experiment  # noqa: E402

__all__ = ["Experiment"]
