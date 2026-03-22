"""
Galileo Future API.

This package provides the next-generation object-centric API for Galileo.
"""

from __future__ import annotations

from galileo.collaborator import Collaborator, CollaboratorRole
from galileo.configuration import Configuration
from galileo.dataset import Dataset
from galileo.experiment import Experiment
from galileo.integration import Integration
from galileo.log_stream import LogStream
from galileo.metric import CodeMetric, GalileoMetric, LlmMetric, LocalMetric, Metric
from galileo.model import Model
from galileo.project import Project
from galileo.prompt import Prompt
from galileo.schema.message import Message
from galileo.search import RecordType
from galileo.shared.exceptions import (
    APIError,
    ConfigurationError,
    GalileoFutureError,
    ResourceConflictError,
    ResourceNotFoundError,
    ValidationError,
)
from galileo.utils.log_config import enable_console_logging
from galileo_core.schemas.logging.llm import MessageRole
from galileo_core.schemas.logging.step import StepType

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
