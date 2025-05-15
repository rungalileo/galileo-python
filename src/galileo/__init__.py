"""Galileo"""

# flake8: noqa: F401
# ruff: noqa: F401

from galileo.decorator import GalileoDecorator, galileo_context, log
from galileo.logger import GalileoLogger
from galileo.schema.message import Message
from galileo_core.helpers.api_key import create_api_key, delete_api_key, list_api_keys
from galileo_core.helpers.dependencies import is_dependency_available
from galileo_core.schemas.logging.llm import MessageRole, ToolCall, ToolCallFunction
from galileo_core.schemas.logging.span import LlmSpan, RetrieverSpan, Span, StepWithChildSpans, ToolSpan, WorkflowSpan
from galileo_core.schemas.logging.step import StepType
from galileo_core.schemas.logging.trace import Trace

__version__ = "0.9.1"
