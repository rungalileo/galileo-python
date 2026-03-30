"""Deprecated: use galileo.shared.experiment_result instead of galileo.__future__.shared.experiment_result."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.shared.experiment_result is deprecated. "
    "Use galileo.shared.experiment_result instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.shared.experiment_result import (  # noqa: E402
    ExperimentPhaseInfo,
    ExperimentRunResult,
    ExperimentStatusInfo,
)

__all__ = ["ExperimentPhaseInfo", "ExperimentRunResult", "ExperimentStatusInfo"]
