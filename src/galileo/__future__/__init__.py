"""
Galileo Future API.

This package provides the next-generation object-centric API for Galileo.
"""

from galileo.__future__.configuration import Configuration
from galileo.__future__.dataset import Dataset
from galileo.__future__.exceptions import (
    APIError,
    ConfigurationError,
    GalileoFutureError,
    ResourceConflictError,
    ResourceNotFoundError,
    ValidationError,
)
from galileo.__future__.log_stream import LogStream
from galileo.__future__.metric import Metric
from galileo.__future__.project import Project
from galileo.__future__.prompt import Prompt
from galileo.__future__.types import MetricSpec
from galileo.schema.message import Message
from galileo.schema.metrics import GalileoScorers, LocalMetricConfig
from galileo.utils.logging import enable_console_logging
from galileo_core.schemas.logging.llm import MessageRole
from galileo_core.schemas.logging.step import StepType

__all__ = [
    "APIError",
    "Configuration",
    "ConfigurationError",
    "Dataset",
    "GalileoFutureError",
    "GalileoScorers",
    "LocalMetricConfig",
    "LogStream",
    "Message",
    "MessageRole",
    "Metric",
    "MetricSpec",
    "Project",
    "Prompt",
    "ResourceConflictError",
    "ResourceNotFoundError",
    "StepType",
    "ValidationError",
    "enable_console_logging",
]
