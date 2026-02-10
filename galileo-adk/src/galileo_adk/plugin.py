"""Galileo ADK Plugin - Runner-level observability for Google ADK."""

from __future__ import annotations

import logging
import os
import re
from collections.abc import Callable
from typing import Any
from uuid import UUID

from galileo.schema.trace import TracesIngestRequest
from galileo_adk.observer import (
    GalileoObserver,
    get_agent_name_from_tool_context,
    get_custom_metadata,
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

    # Try to parse from error message
    error_str = str(error)
    # Match leading HTTP status code (e.g., "429 RESOURCE_EXHAUSTED")
    match = re.match(r"(\d{3})\s", error_str)
    if match:
        code = int(match.group(1))
        if _is_http_status_code(code):
            return code
    # Match "HTTP <code>" or "status[: ]<code>" patterns
    match = re.search(r"(?:HTTP\s*|status[:\s]+)(\d{3})\b", error_str, re.IGNORECASE)
    if match:
        code = int(match.group(1))
        if _is_http_status_code(code):
            return code

    return 500


class GalileoADKPlugin(BasePlugin):
    """Galileo observability plugin for Google ADK Runner.

    Provides full lifecycle observability including invocation, agent, LLM, and tool
    spans. Pass to Runner's plugins list for automatic trace capture.

    ADK session_id is automatically mapped to Galileo sessions for trace grouping.
    All traces from the same ADK session will be grouped together in Galileo.

    Per-invocation metadata is passed via ADK's native RunConfig.custom_metadata:

        run_config = RunConfig(custom_metadata={"turn": 1, "user_id": "abc"})
        await runner.run_async(..., run_config=run_config)

    Parameters
    ----------
    project : str, optional
        Galileo project name. Can also be set via GALILEO_PROJECT env var.
        Required unless `ingestion_hook` is provided.
    log_stream : str, optional
        Log stream name within the project. Can also be set via GALILEO_LOG_STREAM env var.
        Required unless `ingestion_hook` is provided.
    ingestion_hook : Callable[[TracesIngestRequest], None], optional
        Custom callback to receive trace data instead of sending to Galileo.

    Example
    -------
    >>> plugin = GalileoADKPlugin(project="my-project", log_stream="production")
    >>> runner = Runner(agent=agent, plugins=[plugin])
    >>> run_config = RunConfig(custom_metadata={"turn": 1})
    >>> await runner.run_async(..., run_config=run_config)
    """

    def __init__(
        self,
        project: str | None = None,
        log_stream: str | None = None,
        ingestion_hook: Callable[[TracesIngestRequest], None] | None = None,
    ) -> None:
        effective_project = project or os.environ.get("GALILEO_PROJECT")
        effective_log_stream = log_stream or os.environ.get("GALILEO_LOG_STREAM")
        if not ingestion_hook and (not effective_project or not effective_log_stream):
            raise ValueError(
                "Both 'project' and 'log_stream' must be provided via parameters or "
                "GALILEO_PROJECT/GALILEO_LOG_STREAM environment variables"
            )

        super().__init__(name="galileo")
        self._observer = GalileoObserver(
            project=project,
            log_stream=log_stream,
            ingestion_hook=ingestion_hook,
        )
        self._tracker = SpanTracker()

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
            _logger.debug("_get_parent_agent_run_id: %s", e)

        # Fall back to root invocation run
        return self._tracker.get_run(invocation_id)

    @staticmethod
    def _get_current_agent_name_from_tool_context(tool_context: ToolContext) -> str | None:
        """Extract current agent name from tool context."""
        return get_agent_name_from_tool_context(tool_context)

    async def on_user_message_callback(
        self, *, invocation_context: InvocationContext, user_message: Content
    ) -> Content | None:
        """Capture user message and start run span (invocation wrapper)."""
        try:
            invocation_id = get_invocation_id(invocation_context)
            session_id = get_session_id(invocation_context)

            # Sub-invocation: active tool on current session means AgentTool spawned a sub-agent
            current_session = self._observer.current_adk_session
            is_sub_invocation = (
                current_session is not None and self._tracker.get_active_tool(current_session) is not None
            )
            self._observer.update_session_if_changed(session_id, is_sub_invocation=is_sub_invocation)

            metadata = get_custom_metadata(invocation_context)
            self._observer.store_invocation_metadata(invocation_id, session_id, metadata)

            root_session = self._observer.current_adk_session or session_id
            parent_run_id = self._tracker.get_active_tool(root_session)

            run_id = self._observer.on_run_start(invocation_context, user_message, parent_run_id, metadata=metadata)
            self._tracker.register_run(invocation_id, session_id, run_id)
        except Exception as e:
            _logger.error("on_user_message_callback failed: %s", e, exc_info=True)
        return None

    async def before_run_callback(self, *, invocation_context: InvocationContext) -> None:
        """Update run span name to reflect ADK's routed agent.

        ADK may replace invocation_context.agent between on_user_message_callback
        and before_run_callback via _find_agent_to_run.
        """
        try:
            invocation_id = get_invocation_id(invocation_context)
            actual_agent = getattr(getattr(invocation_context, "agent", None), "name", None)
            run_id = self._tracker.get_run(invocation_id)
            if run_id and actual_agent:
                node = self._observer.handler.get_node(run_id)
                if node:
                    node.span_params["name"] = f"invocation [{actual_agent}]"
                    metadata = node.span_params.get("metadata", {}) or {}
                    metadata["adk_routed_agent"] = actual_agent
                    node.span_params["metadata"] = metadata
        except Exception as e:
            _logger.debug("before_run_callback: %s", e)

    async def after_run_callback(self, *, invocation_context: InvocationContext) -> None:
        """Close run span and flush traces to Galileo."""
        try:
            invocation_id = get_invocation_id(invocation_context)

            # Clean up orphaned spans
            orphaned_tools = self._tracker.pop_all_tools_for_invocation(invocation_id)
            for tool_run_id in orphaned_tools:
                self._observer.force_end_tool(run_id=tool_run_id, output="", status_code=500)

            orphaned_llms = self._tracker.pop_all_llms_for_invocation(invocation_id)
            for llm_run_id in orphaned_llms:
                self._observer.force_end_llm(run_id=llm_run_id, output=None, status_code=500)
            self._tracker.clear_all_llm_call_ids_for_invocation(invocation_id)

            orphaned_agents = self._tracker.pop_all_agents_for_invocation(invocation_id)
            for agent_run_id in orphaned_agents:
                self._observer.force_end_agent(run_id=agent_run_id, output="", status_code=500)

            run_id = self._tracker.pop_run(invocation_id)
            if run_id:
                output = self._observer._extract_final_output(invocation_context)
                self._observer.on_run_end(run_id=run_id, output=output)

            self._observer.cleanup_invocation_metadata(invocation_id)
        except Exception as e:
            _logger.error("after_run_callback failed: %s", e, exc_info=True)

    async def before_agent_callback(self, *, callback_context: CallbackContext, **kwargs: Any) -> Content | None:
        """Start agent span for observability."""
        try:
            invocation_id = get_invocation_id(callback_context)
            session_id = get_session_id(callback_context)
            agent_name = getattr(callback_context, "agent_name", "unknown")
            parent_run_id = self._get_parent_agent_run_id(callback_context)

            metadata = self._observer.get_invocation_metadata(invocation_id, session_id)
            run_id = self._observer.on_agent_start(callback_context, parent_run_id, metadata=metadata)
            self._tracker.register_agent(invocation_id, agent_name, run_id)
        except Exception as e:
            _logger.error("before_agent_callback failed: %s", e, exc_info=True)
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
            _logger.error("after_agent_callback failed: %s", e, exc_info=True)
        return None

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> LlmResponse | None:
        """Handle LLM call start. Creates an LLM span for observability."""
        try:
            invocation_id = get_invocation_id(callback_context)
            session_id = get_session_id(callback_context)
            agent_name = getattr(callback_context, "agent_name", "unknown")
            parent_run_id = self._tracker.get_agent(invocation_id, agent_name)

            metadata = self._observer.get_invocation_metadata(invocation_id, session_id)
            run_id = self._observer.on_llm_start(callback_context, llm_request, parent_run_id, metadata=metadata)
            # Store call_id for response correlation
            call_id = self._tracker.resolve_llm_call_id(llm_request, invocation_id)
            self._tracker.store_call_id(llm_request, call_id)
            self._tracker.set_current_llm_call_id(invocation_id, call_id)
            self._tracker.register_llm(invocation_id, call_id, run_id)
        except Exception as e:
            _logger.error("before_model_callback failed: %s", e, exc_info=True)
        return None

    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse
    ) -> LlmResponse | None:
        """Handle LLM call end. Closes the LLM span and extracts token usage metrics."""
        try:
            invocation_id = get_invocation_id(callback_context)
            call_id = self._tracker.resolve_llm_call_id(llm_response, invocation_id)
            run_id = self._tracker.pop_llm(invocation_id, call_id)
            if run_id:
                self._observer.on_llm_end(run_id, llm_response)
            self._tracker.clear_current_llm_call_id(invocation_id)
        except Exception as e:
            _logger.error("after_model_callback failed: %s", e, exc_info=True)
        return None

    async def on_model_error_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest, error: Exception
    ) -> LlmResponse | None:
        """Handle LLM errors. Closes the LLM span with error status code."""
        try:
            invocation_id = get_invocation_id(callback_context)
            call_id = self._tracker.resolve_llm_call_id(llm_request, invocation_id)
            status_code = _extract_status_code(error)
            run_id = self._tracker.pop_llm(invocation_id, call_id)
            self._tracker.clear_current_llm_call_id(invocation_id)
            if run_id:
                self._observer.on_llm_end(run_id, None, status_code=status_code)

            # Force commit on fatal errors that will abort the run
            if self._is_fatal_error(status_code):
                self._force_commit_partial_trace(invocation_id, error, status_code)
        except Exception as e:
            _logger.error("on_model_error_callback failed: %s", e, exc_info=True)
        return None

    def _is_fatal_error(self, status_code: int) -> bool:
        """Check if error will cause runner to abort (not retry).

        ADK does not retry model errors. 401/403/429 are non-retryable at the
        application level, so we force-commit partial traces for these.
        """
        return status_code in (401, 403, 429)

    def _force_commit_partial_trace(self, invocation_id: str, error: Exception, status_code: int) -> None:
        """End all open spans and commit partial trace on fatal error."""
        error_output = f"Error: {error}"

        tool_run_ids = self._tracker.pop_all_tools_for_invocation(invocation_id)
        for tool_run_id in tool_run_ids:
            self._observer.force_end_tool(run_id=tool_run_id, output=error_output, status_code=status_code)

        llm_run_ids = self._tracker.pop_all_llms_for_invocation(invocation_id)
        for llm_run_id in llm_run_ids:
            self._observer.force_end_llm(run_id=llm_run_id, output=None, status_code=status_code)
        self._tracker.clear_all_llm_call_ids_for_invocation(invocation_id)

        agent_run_ids = self._tracker.pop_all_agents_for_invocation(invocation_id)
        for agent_run_id in agent_run_ids:
            self._observer.force_end_agent(run_id=agent_run_id, output=error_output, status_code=status_code)

        run_id = self._tracker.pop_run(invocation_id)
        if run_id:
            self._observer.force_end_run(run_id=run_id, output=error_output, status_code=status_code)

    async def before_tool_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext
    ) -> dict[str, Any] | None:
        """Start tool span for observability."""
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            session_id = get_tool_session_id(tool_context)
            agent_name = self._get_current_agent_name_from_tool_context(tool_context)

            # Use root session for consistent tracking across sub-invocations
            root_session = self._observer.current_adk_session or session_id

            # Parent resolution: agent span → invocation run → active tool
            parent_run_id = None
            if agent_name:
                parent_run_id = self._tracker.get_agent(invocation_id, agent_name)
            if not parent_run_id:
                parent_run_id = self._tracker.get_run(invocation_id)
            if not parent_run_id and root_session:
                parent_run_id = self._tracker.get_active_tool(root_session)

            metadata = self._observer.get_invocation_metadata(invocation_id, session_id)
            run_id = self._observer.on_tool_start(tool, tool_args, tool_context, parent_run_id, metadata=metadata)
            tool_key = self._tracker.make_tool_key(tool)
            self._tracker.register_tool(invocation_id, tool_key, run_id)
            if root_session:
                self._tracker.set_active_tool(root_session, run_id)
        except Exception as e:
            _logger.error("before_tool_callback failed: %s", e, exc_info=True)
        return None

    async def after_tool_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext, result: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Close tool span."""
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            session_id = get_tool_session_id(tool_context)
            tool_key = self._tracker.make_tool_key(tool)
            run_id = self._tracker.pop_tool(invocation_id, tool_key)

            if run_id:
                self._observer.on_tool_end(run_id, result)
                root_session = self._observer.current_adk_session or session_id
                if root_session:
                    self._tracker.clear_active_tool(root_session, run_id)
        except Exception as e:
            _logger.error("after_tool_callback failed: %s", e, exc_info=True)
        return None

    async def on_tool_error_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext, error: Exception
    ) -> dict[str, Any] | None:
        """Close tool span with error status code."""
        error_response = {"error": str(error)}
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            session_id = get_tool_session_id(tool_context)
            tool_key = self._tracker.make_tool_key(tool)
            run_id = self._tracker.pop_tool(invocation_id, tool_key)
            if run_id:
                status_code = _extract_status_code(error)
                self._observer.on_tool_end(run_id, error_response, status_code=status_code)
                root_session = self._observer.current_adk_session or session_id
                if root_session:
                    self._tracker.clear_active_tool(root_session, run_id)
        except Exception as e:
            _logger.error("on_tool_error_callback failed: %s", e, exc_info=True)
        return error_response

    async def on_event_callback(self, *, invocation_context: InvocationContext, event: Event) -> Event | None:
        """No-op handler for streaming events."""
        return None
