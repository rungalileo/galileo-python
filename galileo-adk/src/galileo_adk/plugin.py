"""Galileo ADK Plugin - Runner-level observability for Google ADK."""

import logging
import re
from collections.abc import Callable
from typing import Any
from uuid import UUID

from galileo.logger import GalileoLogger
from galileo.schema.trace import TracesIngestRequest
from galileo_adk.observer import (
    GalileoObserver,
    get_invocation_id,
    get_session_id,
    get_tool_invocation_id,
    get_tool_session_id,
)
from galileo_adk.span_tracker import SpanTracker

try:
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.agents.invocation_context import InvocationContext
    from google.adk.events import Event
    from google.adk.models import LlmRequest, LlmResponse
    from google.adk.plugins import BasePlugin
    from google.adk.tools import BaseTool
    from google.adk.tools.tool_context import ToolContext
    from google.genai.types import Content
except ImportError:
    BasePlugin = object  # type: ignore[assignment,misc]
    CallbackContext = object  # type: ignore[assignment,misc]
    InvocationContext = object  # type: ignore[assignment,misc]
    Event = object  # type: ignore[assignment,misc]
    LlmRequest = object  # type: ignore[assignment,misc]
    LlmResponse = object  # type: ignore[assignment,misc]
    BaseTool = object  # type: ignore[assignment,misc]
    ToolContext = object  # type: ignore[assignment,misc]
    Content = object  # type: ignore[assignment,misc]

_logger = logging.getLogger(__name__)


def _is_http_status_code(code: int) -> bool:
    """Check if code is a valid HTTP status code (100-599)."""
    return 100 <= code <= 599


def _extract_status_code(error: Exception) -> int:
    """Extract HTTP status code from exception, defaulting to 500."""

    # Try error.code (may be int or enum)
    if hasattr(error, "code"):
        code = error.code
        if isinstance(code, int) and _is_http_status_code(code):
            return code
        # Handle enum-like objects with .value
        if hasattr(code, "value") and isinstance(code.value, int) and _is_http_status_code(code.value):
            return code.value
        # Try to convert to int
        try:
            code_int = int(code)
            if _is_http_status_code(code_int):
                return code_int
        except (ValueError, TypeError):
            pass

    # Try error.status_code
    if hasattr(error, "status_code"):
        status_code = error.status_code
        if isinstance(status_code, int) and _is_http_status_code(status_code):
            return status_code
        try:
            code_int = int(status_code)
            if _is_http_status_code(code_int):
                return code_int
        except (ValueError, TypeError):
            pass

    # Try to parse from error message (e.g., "429 RESOURCE_EXHAUSTED")
    error_str = str(error)
    match = re.search(r"\b(4\d{2}|5\d{2})\b", error_str)
    if match:
        return int(match.group(1))

    return 500


class GalileoADKPlugin(BasePlugin):
    """Galileo observability plugin for Google ADK Runner.

    Provides full lifecycle observability including invocation, agent, LLM, and tool
    spans. Pass to Runner's plugins list for automatic trace capture.

    ADK session_id is automatically mapped to Galileo sessions for trace grouping.
    All traces from the same ADK session will be grouped together in Galileo.

    Parameters
    ----------
    project : str, optional
        Galileo project name. Required unless `ingestion_hook` is provided.
    log_stream : str, optional
        Log stream name within the project.
    galileo_logger : GalileoLogger, optional
        Pre-configured logger instance.
    start_new_trace : bool, default True
        Whether to start a new trace for each invocation.
    flush_on_run_end : bool, default True
        Whether to flush traces when the run ends.
    ingestion_hook : Callable[[TracesIngestRequest], None], optional
        Custom callback to receive trace data instead of sending to Galileo.
    metadata : dict[str, Any], optional
        Static metadata to attach to all spans.

    Example
    -------
    >>> plugin = GalileoADKPlugin(project="my-project")
    >>> runner = Runner(agent=agent, plugins=[plugin])
    """

    def __init__(
        self,
        project: str | None = None,
        log_stream: str | None = None,
        galileo_logger: GalileoLogger | None = None,
        start_new_trace: bool = True,
        flush_on_run_end: bool = True,
        ingestion_hook: Callable[[TracesIngestRequest], None] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if not ingestion_hook and not project and not galileo_logger:
            raise ValueError("Either 'project' or 'ingestion_hook' must be provided")

        super().__init__(name="galileo")
        self._observer = GalileoObserver(
            project=project,
            log_stream=log_stream,
            galileo_logger=galileo_logger,
            start_new_trace=start_new_trace,
            flush_on_completion=flush_on_run_end,
            ingestion_hook=ingestion_hook,
            metadata=metadata,
        )
        self._metadata: dict[str, Any] = metadata.copy() if metadata else {}
        self._tracker = SpanTracker()

    @property
    def metadata(self) -> dict[str, Any]:
        """Get current metadata that will be attached to all spans."""
        return self._metadata

    @metadata.setter
    def metadata(self, value: dict[str, Any]) -> None:
        """Set metadata for subsequent invocations.

        Set this before each turn to include turn-specific metadata on all spans.

        Example:
            plugin.metadata = {"turn": 1, "thread_id": "abc", "user_tier": "premium"}
            await runner.run_async(...)
        """
        self._metadata = value if value is not None else {}

    def _get_parent_agent_run_id(self, callback_context: CallbackContext) -> UUID | None:
        """Get the run_id of the parent agent, or fall back to root invocation."""
        invocation_id = get_invocation_id(callback_context)

        # Try to get parent agent name from ADK's agent hierarchy
        try:
            inv_ctx = getattr(callback_context, "_invocation_context", None)
            if inv_ctx:
                agent = getattr(inv_ctx, "agent", None)
                if agent:
                    parent_agent = getattr(agent, "parent_agent", None)
                    if parent_agent:
                        parent_name = getattr(parent_agent, "name", None)
                        if parent_name:
                            parent_run_id = self._tracker.get_agent(invocation_id, parent_name)
                            if parent_run_id:
                                return parent_run_id
        except Exception as e:
            _logger.debug(f"Exception getting parent: {e}")

        # Fall back to root invocation run
        return self._tracker.get_run(invocation_id)

    def _get_current_agent_name_from_tool_context(self, tool_context: ToolContext) -> str | None:
        """Extract current agent name from tool context."""
        try:
            # Try callback_context path
            if hasattr(tool_context, "callback_context"):
                return getattr(tool_context.callback_context, "agent_name", None)
            # Try direct agent_name
            if hasattr(tool_context, "agent_name"):
                return getattr(tool_context, "agent_name", None)
        except Exception:
            pass
        return None

    async def on_user_message_callback(
        self, *, invocation_context: InvocationContext, user_message: Content
    ) -> Content | None:
        """Capture user message and start run span (invocation wrapper)."""
        try:
            invocation_id = get_invocation_id(invocation_context)
            session_id = get_session_id(invocation_context)

            self._observer.update_session_if_changed(session_id)

            root_session = self._observer._current_adk_session or session_id
            parent_run_id = self._tracker.get_active_tool(root_session)

            run_id = self._observer.on_run_start(
                invocation_context, user_message, parent_run_id, metadata=self._metadata
            )
            self._tracker.register_run(invocation_id, session_id, run_id)
        except Exception as e:
            _logger.error(f"Error in on_user_message_callback: {e}", exc_info=True)
        return None

    async def before_run_callback(self, *, invocation_context: InvocationContext) -> None:
        """Called before agent processing starts."""
        pass

    async def after_run_callback(self, *, invocation_context: InvocationContext) -> None:
        """Close run span and flush traces to Galileo."""
        try:
            invocation_id = get_invocation_id(invocation_context)

            # Clean up any orphaned spans for this invocation
            orphaned_tools = self._tracker.pop_all_tools_for_invocation(invocation_id)
            for tool_run_id in orphaned_tools:
                self._observer._span_manager.end_tool(run_id=tool_run_id, output="", status_code=500)

            orphaned_llms = self._tracker.pop_all_llms_for_invocation(invocation_id)
            for llm_run_id in orphaned_llms:
                self._observer._span_manager.end_llm(run_id=llm_run_id, output=None, status_code=500)

            orphaned_agents = self._tracker.pop_all_agents_for_invocation(invocation_id)
            for agent_run_id in orphaned_agents:
                self._observer._span_manager.end_agent(run_id=agent_run_id, output="", status_code=500)

            run_id = self._tracker.pop_run(invocation_id)
            if run_id:
                output = self._observer._extract_final_output(invocation_context)
                self._observer.on_run_end(run_id=run_id, output=output)
        except Exception as e:
            _logger.error(f"Error in after_run_callback: {e}", exc_info=True)

    async def before_agent_callback(self, *, callback_context: CallbackContext, **kwargs: Any) -> Content | None:
        """Start agent span for observability."""
        try:
            invocation_id = get_invocation_id(callback_context)
            agent_name = getattr(callback_context, "agent_name", "unknown")
            parent_run_id = self._get_parent_agent_run_id(callback_context)
            run_id = self._observer.on_agent_start(callback_context, parent_run_id, metadata=self._metadata)
            self._tracker.register_agent(invocation_id, agent_name, run_id)
        except Exception as e:
            _logger.error(f"Error in before_agent_callback: {e}", exc_info=True)
        return None

    async def after_agent_callback(self, *, callback_context: CallbackContext, **kwargs: Any) -> Content | None:
        """Close agent span."""
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
        # Fallback to object identity for correlation
        return f"llm_{id(obj)}"

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> LlmResponse | None:
        """Handle LLM call start. Creates an LLM span for observability."""
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

    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse
    ) -> LlmResponse | None:
        """Handle LLM call end. Closes the LLM span and extracts token usage metrics."""
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

    async def on_model_error_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest, error: Exception
    ) -> LlmResponse | None:
        """Handle LLM errors. Closes the LLM span with error status code."""
        try:
            invocation_id = get_invocation_id(callback_context)
            call_id = self._get_llm_call_id(llm_request, invocation_id)
            run_id = self._tracker.pop_llm(invocation_id, call_id)
            self._tracker.clear_current_llm_call_id(invocation_id)
            if run_id:
                status_code = _extract_status_code(error)
                self._observer.on_llm_end(run_id, None, status_code=status_code)

            # Force commit on fatal errors that will abort the run
            if self._is_fatal_error(error):
                self._force_commit_partial_trace(invocation_id, error)
        except Exception as e:
            _logger.error(f"Error in on_model_error_callback: {e}", exc_info=True)
        return None

    def _is_fatal_error(self, error: Exception) -> bool:
        """Check if error will cause runner to abort (not retry)."""
        code = _extract_status_code(error)
        return code in (401, 403, 429)

    def _force_commit_partial_trace(self, invocation_id: str, error: Exception) -> None:
        """End all open spans and commit partial trace on fatal error."""
        error_output = f"Error: {error}"
        status_code = _extract_status_code(error)

        # End any open tool spans for this invocation (also clears active tool via session lookup)
        tool_run_ids = self._tracker.pop_all_tools_for_invocation(invocation_id)
        for tool_run_id in tool_run_ids:
            self._observer._span_manager.end_tool(run_id=tool_run_id, output=error_output, status_code=status_code)

        # End any open LLM spans for this invocation
        llm_run_ids = self._tracker.pop_all_llms_for_invocation(invocation_id)
        for llm_run_id in llm_run_ids:
            self._observer._span_manager.end_llm(run_id=llm_run_id, output=None, status_code=status_code)

        # End any open agent spans for this invocation
        agent_run_ids = self._tracker.pop_all_agents_for_invocation(invocation_id)
        for agent_run_id in agent_run_ids:
            self._observer._span_manager.end_agent(run_id=agent_run_id, output=error_output, status_code=status_code)

        run_id = self._tracker.pop_run(invocation_id)
        if run_id:
            self._observer._span_manager.end_run(run_id=run_id, output=error_output, status_code=status_code)

    def _get_tool_key(self, tool: BaseTool) -> str:
        """Generate a stable tool key from the tool object."""
        tool_name = getattr(tool, "name", "unknown")
        # Use object identity for correlation (same tool object in before/after)
        return f"{tool_name}_{id(tool)}"

    async def before_tool_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext
    ) -> dict[str, Any] | None:
        """Start tool span for observability."""
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            session_id = get_tool_session_id(tool_context)
            agent_name = self._get_current_agent_name_from_tool_context(tool_context)

            root_session = self._observer._current_adk_session or session_id

            # Resolve parent with fallback chain:
            # 1. Current agent span (if agent_name available)
            parent_run_id = None
            if agent_name:
                parent_run_id = self._tracker.get_agent(invocation_id, agent_name)
            # 2. Invocation-level run span (root of this invocation)
            if not parent_run_id:
                parent_run_id = self._tracker.get_run(invocation_id)
            # 3. Active tool in session (for tools called from within other tools)
            if not parent_run_id:
                parent_run_id = self._tracker.get_active_tool(root_session)

            run_id = self._observer.on_tool_start(tool, tool_args, tool_context, parent_run_id, metadata=self._metadata)
            tool_key = self._get_tool_key(tool)
            self._tracker.register_tool(invocation_id, tool_key, run_id)
            self._tracker.set_active_tool(root_session, run_id)
        except Exception as e:
            _logger.error(f"Error in before_tool_callback: {e}", exc_info=True)
        return None

    async def after_tool_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext, result: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Close tool span."""
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            session_id = get_tool_session_id(tool_context)
            tool_key = self._get_tool_key(tool)
            run_id = self._tracker.pop_tool(invocation_id, tool_key)
            if run_id:
                self._observer.on_tool_end(run_id, result)
                root_session = self._observer._current_adk_session or session_id
                self._tracker.clear_active_tool(root_session, run_id)
        except Exception as e:
            _logger.error(f"Error in after_tool_callback: {e}", exc_info=True)
        return None

    async def on_tool_error_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext, error: Exception
    ) -> dict[str, Any] | None:
        """Close tool span with error status code."""
        error_response = {"error": str(error)}
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            session_id = get_tool_session_id(tool_context)
            tool_key = self._get_tool_key(tool)
            run_id = self._tracker.pop_tool(invocation_id, tool_key)
            if run_id:
                status_code = _extract_status_code(error)
                self._observer.on_tool_end(run_id, error_response, status_code=status_code)
                root_session = self._observer._current_adk_session or session_id
                self._tracker.clear_active_tool(root_session, run_id)
        except Exception as e:
            _logger.error(f"Error in on_tool_error_callback: {e}", exc_info=True)
        return error_response

    async def on_event_callback(self, *, invocation_context: InvocationContext, event: Event) -> Event | None:
        """Capture streaming events."""
        try:
            invocation_id = get_invocation_id(invocation_context)
            run_id = self._tracker.get_run(invocation_id)
            if run_id:
                self._observer.on_event(run_id, event)
        except Exception as e:
            _logger.error(f"Error in on_event_callback: {e}", exc_info=True)
        return None
