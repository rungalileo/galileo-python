"""Galileo ADK Callback - Agent-level observability for Google ADK."""

import logging
from collections.abc import Callable
from typing import Any

from galileo.logger import GalileoLogger
from galileo.schema.trace import TracesIngestRequest
from galileo_adk.observer import GalileoObserver, get_invocation_id, get_tool_invocation_id
from galileo_adk.span_tracker import SpanTracker

try:
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.models import LlmRequest, LlmResponse
    from google.adk.tools import BaseTool
    from google.adk.tools.tool_context import ToolContext
except ImportError:
    CallbackContext = object  # type: ignore[assignment,misc]
    LlmRequest = object  # type: ignore[assignment,misc]
    LlmResponse = object  # type: ignore[assignment,misc]
    BaseTool = object  # type: ignore[assignment,misc]
    ToolContext = object  # type: ignore[assignment,misc]

_logger = logging.getLogger(__name__)


class GalileoADKCallback:
    """Galileo observability callbacks for Google ADK agents.

    Use this class when you need agent-level callbacks (passed directly to Agent
    constructors). For runner-level observability with full lifecycle tracking,
    use GalileoADKPlugin instead.

    Parameters
    ----------
    project : str, optional
        Galileo project name. Required unless `ingestion_hook` or
        `galileo_logger` is provided.
    log_stream : str, optional
        Log stream name within the project.
    galileo_logger : GalileoLogger, optional
        Pre-configured logger instance.
    start_new_trace : bool, default True
        Whether to start a new trace for each agent invocation.
    flush_on_agent_end : bool, default True
        Whether to flush traces to Galileo when the agent ends.
    ingestion_hook : Callable[[TracesIngestRequest], None], optional
        Custom callback to receive trace data instead of sending to Galileo.
    external_id : str, optional
        External identifier for session grouping.
    metadata : dict[str, Any], optional
        Static metadata to attach to all spans.

    Example
    -------
    >>> callback = GalileoADKCallback(project="my-project")
    >>> agent = Agent(
    ...     before_agent_callback=callback.before_agent_callback,
    ...     after_agent_callback=callback.after_agent_callback,
    ... )
    """

    def __init__(
        self,
        project: str | None = None,
        log_stream: str | None = None,
        galileo_logger: GalileoLogger | None = None,
        start_new_trace: bool = True,
        flush_on_agent_end: bool = True,
        ingestion_hook: Callable[[TracesIngestRequest], None] | None = None,
        external_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if not ingestion_hook and not project and not galileo_logger:
            raise ValueError("Either 'project' or 'ingestion_hook' must be provided")

        self._observer = GalileoObserver(
            project=project,
            log_stream=log_stream,
            galileo_logger=galileo_logger,
            start_new_trace=start_new_trace,
            flush_on_completion=flush_on_agent_end,
            ingestion_hook=ingestion_hook,
            external_id=external_id,
            metadata=metadata,
        )
        self._metadata: dict[str, Any] = metadata.copy() if metadata else {}
        self._tracker = SpanTracker()

    @property
    def _handler(self) -> Any:
        """Access the underlying handler (for tests)."""
        return self._observer.handler

    @property
    def metadata(self) -> dict[str, Any]:
        """Get current metadata that will be attached to all spans."""
        return self._metadata

    @metadata.setter
    def metadata(self, value: dict[str, Any]) -> None:
        """Set metadata for subsequent agent runs."""
        self._metadata = value if value is not None else {}

    def before_agent_callback(self, callback_context: CallbackContext) -> Any | None:
        """Start agent span for observability."""
        try:
            invocation_id = get_invocation_id(callback_context)
            agent_name = getattr(callback_context, "agent_name", "unknown")
            run_id = self._observer.on_agent_start(callback_context, parent_run_id=None, metadata=self._metadata)
            self._tracker.register_agent(invocation_id, agent_name, run_id)
        except Exception as e:
            _logger.error(f"Error in before_agent_callback: {e}", exc_info=True)
        return None

    def after_agent_callback(self, callback_context: CallbackContext) -> Any | None:
        """Close agent span and flush traces."""
        try:
            invocation_id = get_invocation_id(callback_context)
            agent_name = getattr(callback_context, "agent_name", "unknown")
            run_id = self._tracker.pop_agent(invocation_id, agent_name)
            if run_id:
                self._observer.on_agent_end(run_id, callback_context)
        except Exception as e:
            _logger.error(f"Error in after_agent_callback: {e}", exc_info=True)
        return None

    def _get_llm_call_id(self, obj: Any, invocation_id: str | None = None) -> str:
        """Extract call_id from LlmRequest or LlmResponse, with fallback."""
        # Try stored _galileo_call_id (set by before_model_callback)
        galileo_call_id = getattr(obj, "_galileo_call_id", None)
        if galileo_call_id:
            return galileo_call_id
        # Try request_id (common correlation field in ADK)
        request_id = getattr(obj, "request_id", None)
        if request_id:
            return str(request_id)
        # For responses, check tracker for current call_id
        if invocation_id:
            current_call_id = self._tracker.get_current_llm_call_id(invocation_id)
            if current_call_id:
                return current_call_id
        return f"llm_{id(obj)}"

    def before_model_callback(self, callback_context: CallbackContext, llm_request: LlmRequest) -> LlmResponse | None:
        """Start LLM span for observability."""
        try:
            invocation_id = get_invocation_id(callback_context)
            agent_name = getattr(callback_context, "agent_name", "unknown")
            parent_run_id = self._tracker.get_agent(invocation_id, agent_name)
            run_id = self._observer.on_llm_start(callback_context, llm_request, parent_run_id, metadata=self._metadata)
            # Generate stable call_id and store for response correlation
            call_id = self._get_llm_call_id(llm_request, invocation_id)
            llm_request._galileo_call_id = call_id
            self._tracker.set_current_llm_call_id(invocation_id, call_id)
            self._tracker.register_llm(invocation_id, call_id, run_id)
        except Exception as e:
            _logger.error(f"Error in before_model_callback: {e}", exc_info=True)
        return None

    def after_model_callback(self, callback_context: CallbackContext, llm_response: LlmResponse) -> LlmResponse | None:
        """Close LLM span and extract token usage metrics."""
        try:
            invocation_id = get_invocation_id(callback_context)
            call_id = self._get_llm_call_id(llm_response, invocation_id)
            run_id = self._tracker.pop_llm(invocation_id, call_id)
            if run_id:
                self._observer.on_llm_end(run_id, llm_response)
            self._tracker.clear_current_llm_call_id(invocation_id)
        except Exception as e:
            _logger.error(f"Error in after_model_callback: {e}", exc_info=True)
        return None

    def _get_agent_name_from_tool_context(self, tool_context: ToolContext) -> str:
        """Extract agent name from tool context."""
        try:
            if hasattr(tool_context, "callback_context"):
                return getattr(tool_context.callback_context, "agent_name", "unknown")
            if hasattr(tool_context, "agent_name"):
                return getattr(tool_context, "agent_name", "unknown")
        except Exception:
            pass
        return "unknown"

    def _get_tool_key(self, tool: BaseTool) -> str:
        """Generate a stable tool key from the tool object."""
        tool_name = getattr(tool, "name", "unknown")
        return f"{tool_name}_{id(tool)}"

    def before_tool_callback(
        self, tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
    ) -> dict[str, Any] | None:
        """Start tool span for observability."""
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            agent_name = self._get_agent_name_from_tool_context(tool_context)
            parent_run_id = self._tracker.get_agent(invocation_id, agent_name)
            run_id = self._observer.on_tool_start(tool, args, tool_context, parent_run_id, metadata=self._metadata)
            tool_key = self._get_tool_key(tool)
            self._tracker.register_tool(invocation_id, tool_key, run_id)
        except Exception as e:
            _logger.error(f"Error in before_tool_callback: {e}", exc_info=True)
        return None

    def after_tool_callback(
        self, tool: BaseTool, args: dict[str, Any], tool_context: ToolContext, tool_response: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Close tool span."""
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            tool_key = self._get_tool_key(tool)
            run_id = self._tracker.pop_tool(invocation_id, tool_key)
            if run_id:
                self._observer.on_tool_end(run_id, tool_response)
        except Exception as e:
            _logger.error(f"Error in after_tool_callback: {e}", exc_info=True)
        return None
