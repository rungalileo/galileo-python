"""Galileo ADK Callback - Agent-level observability for Google ADK."""

from __future__ import annotations

import logging
import os
from collections.abc import Callable
from typing import Any

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
    >>> callback = GalileoADKCallback(project="my-project", log_stream="production")
    >>> agent = Agent(
    ...     before_agent_callback=callback.before_agent_callback,
    ...     after_agent_callback=callback.after_agent_callback,
    ... )
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

        self._observer = GalileoObserver(
            project=project,
            log_stream=log_stream,
            ingestion_hook=ingestion_hook,
        )
        self._tracker = SpanTracker()

    @property
    def _handler(self) -> Any:
        """Access the underlying handler (for tests)."""
        return self._observer.handler

    def before_agent_callback(self, callback_context: CallbackContext) -> Any | None:
        """Start agent span for observability."""
        try:
            invocation_id = get_invocation_id(callback_context)
            session_id = get_session_id(callback_context)

            # Callback mode cannot detect sub-invocations; use Plugin for multi-agent scenarios.
            self._observer.update_session_if_changed(session_id, is_sub_invocation=False)

            metadata = get_custom_metadata(callback_context)
            self._observer.store_invocation_metadata(invocation_id, session_id, metadata)

            agent_name = getattr(callback_context, "agent_name", "unknown")
            run_id = self._observer.on_agent_start(callback_context, parent_run_id=None, metadata=metadata)
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

            self._observer.cleanup_invocation_metadata(invocation_id)
        except Exception as e:
            _logger.error(f"Error in after_agent_callback: {e}", exc_info=True)
        return None

    def before_model_callback(self, callback_context: CallbackContext, llm_request: LlmRequest) -> LlmResponse | None:
        """Start LLM span for observability."""
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
            _logger.error(f"Error in before_model_callback: {e}", exc_info=True)
        return None

    def after_model_callback(self, callback_context: CallbackContext, llm_response: LlmResponse) -> LlmResponse | None:
        """Close LLM span and extract token usage metrics."""
        try:
            invocation_id = get_invocation_id(callback_context)
            call_id = self._tracker.resolve_llm_call_id(llm_response, invocation_id)
            run_id = self._tracker.pop_llm(invocation_id, call_id)
            if run_id:
                self._observer.on_llm_end(run_id, llm_response)
            self._tracker.clear_current_llm_call_id(invocation_id)
        except Exception as e:
            _logger.error(f"Error in after_model_callback: {e}", exc_info=True)
        return None

    def before_tool_callback(
        self, tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
    ) -> dict[str, Any] | None:
        """Start tool span for observability."""
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            session_id = get_tool_session_id(tool_context)
            agent_name = get_agent_name_from_tool_context(tool_context) or "unknown"
            parent_run_id = self._tracker.get_agent(invocation_id, agent_name)

            metadata = self._observer.get_invocation_metadata(invocation_id, session_id)

            run_id = self._observer.on_tool_start(tool, args, tool_context, parent_run_id, metadata=metadata)
            tool_key = self._tracker.make_tool_key(tool)
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
            tool_key = self._tracker.make_tool_key(tool)
            run_id = self._tracker.pop_tool(invocation_id, tool_key)
            if run_id:
                self._observer.on_tool_end(run_id, tool_response)
        except Exception as e:
            _logger.error(f"Error in after_tool_callback: {e}", exc_info=True)
        return None
