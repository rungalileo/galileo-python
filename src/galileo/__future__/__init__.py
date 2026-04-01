"""Deprecated: use the galileo top-level package instead of galileo.__future__."""

from __future__ import annotations

import warnings

warnings.warn(
    "Importing from galileo.__future__ is deprecated. Use the galileo top-level package instead "
    "(e.g., 'from galileo import Project').",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.collaborator import Collaborator, CollaboratorRole  # noqa: E402
from galileo.configuration import Configuration  # noqa: E402
from galileo.dataset import Dataset  # noqa: E402
from galileo.experiment import Experiment  # noqa: E402
from galileo.integration import Integration  # noqa: E402
from galileo.log_stream import LogStream  # noqa: E402
from galileo.metric import CodeMetric, GalileoMetric, LlmMetric, LocalMetric, Metric  # noqa: E402
from galileo.model import Model  # noqa: E402
from galileo.project import Project  # noqa: E402
from galileo.prompt import Prompt  # noqa: E402
from galileo.schema.message import Message  # noqa: E402
from galileo.search import RecordType  # noqa: E402
from galileo.shared.exceptions import (  # noqa: E402
    APIError,
    ConfigurationError,
    GalileoFutureError,
    ResourceConflictError,
    ResourceNotFoundError,
    ValidationError,
)
from galileo.utils.log_config import enable_console_logging  # noqa: E402
from galileo_core.schemas.logging.llm import MessageRole  # noqa: E402
from galileo_core.schemas.logging.step import StepType  # noqa: E402

__all__ = [
    "APIError",
    "CodeMetric",
    "Collaborator",
    "CollaboratorRole",
    "Configuration",
    "ConfigurationError",
    "Dataset",
    "Experiment",
    "GalileoFutureError",
    "GalileoMetric",
    "Integration",
    "LlmMetric",
    "LocalMetric",
    "LogStream",
    "Message",
    "MessageRole",
    "Metric",
    "Model",
    "Project",
    "Prompt",
    "RecordType",
    "ResourceConflictError",
    "ResourceNotFoundError",
    "StepType",
    "ValidationError",
    "enable_console_logging",
]
