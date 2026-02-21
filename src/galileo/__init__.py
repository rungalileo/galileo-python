"""Galileo."""

from galileo.decorator import GalileoDecorator, galileo_context, log, start_session
from galileo.exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    GalileoAPIError,
    GalileoLoggerException,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from galileo.logger import GalileoLogger
from galileo.protect import ainvoke_protect, invoke_protect
from galileo.schema.message import Message
from galileo.schema.metrics import GalileoMetrics, GalileoScorers
from galileo.stages import (
    create_protect_stage,
    get_protect_stage,
    pause_protect_stage,
    resume_protect_stage,
    update_protect_stage,
)
from galileo.tracing import get_tracing_headers
from galileo.utils.log_config import enable_console_logging
from galileo_core.helpers.api_key import create_api_key, delete_api_key, list_api_keys
from galileo_core.helpers.dependencies import is_dependency_available
from galileo_core.schemas.logging.llm import MessageRole, ToolCall, ToolCallFunction
from galileo_core.schemas.logging.session import Session
from galileo_core.schemas.logging.span import (
    AgentSpan,
    LlmSpan,
    RetrieverSpan,
    Span,
    StepWithChildSpans,
    ToolSpan,
    WorkflowSpan,
)
from galileo_core.schemas.logging.step import StepType
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.protect.execution_status import ExecutionStatus
from galileo_core.schemas.protect.payload import Payload
from galileo_core.schemas.protect.request import Request
from galileo_core.schemas.protect.response import Response
from galileo_core.schemas.protect.ruleset import Ruleset
from galileo_core.schemas.protect.stage import StageType

__version__ = "1.47.0"

__all__ = [
    "AgentSpan",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "ExecutionStatus",
    "ForbiddenError",
    "GalileoAPIError",
    "GalileoDecorator",
    "GalileoLogger",
    "GalileoLoggerException",
    "GalileoMetrics",
    "GalileoScorers",
    "LlmSpan",
    "Message",
    "MessageRole",
    "NotFoundError",
    "Payload",
    "RateLimitError",
    "Request",
    "Response",
    "RetrieverSpan",
    "Ruleset",
    "ServerError",
    "Session",
    "Span",
    "StageType",
    "StepType",
    "StepWithChildSpans",
    "ToolCall",
    "ToolCallFunction",
    "ToolSpan",
    "Trace",
    "WorkflowSpan",
    "ainvoke_protect",
    "create_api_key",
    "create_protect_stage",
    "delete_api_key",
    "enable_console_logging",
    "galileo_context",
    "get_protect_stage",
    "get_tracing_headers",
    "invoke_protect",
    "is_dependency_available",
    "list_api_keys",
    "log",
    "pause_protect_stage",
    "resume_protect_stage",
    "start_session",
    "update_protect_stage",
]
