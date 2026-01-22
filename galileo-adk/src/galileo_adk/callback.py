"""Galileo ADK Callback - Agent-level observability for Google ADK."""

import logging
from collections.abc import Callable
from typing import Any
from uuid import UUID

from galileo.logger import GalileoLogger
from galileo.schema.trace import TracesIngestRequest
from galileo_adk.observer import GalileoObserver, get_invocation_id, get_tool_invocation_id

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
    """Galileo observability callbacks for Google ADK agents."""

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
        self._agent_run_ids: dict[str, UUID] = {}
        self._llm_run_ids: dict[str, UUID] = {}
        self._tool_run_ids: dict[str, UUID] = {}

    @property
    def _handler(self) -> Any:
        """Access the underlying handler (for tests)."""
        return self._observer.handler

    def before_agent_callback(self, callback_context: CallbackContext) -> Any | None:
        """Handle agent start."""
        try:
            run_id = self._observer.on_agent_start(callback_context, parent_run_id=None)
            invocation_id = get_invocation_id(callback_context)
            self._agent_run_ids[invocation_id] = run_id
            callback_context._galileo_run_id = run_id  # type: ignore[attr-defined]
        except Exception as e:
            _logger.error(f"Error in before_agent_callback: {e}", exc_info=True)
        return None

    def after_agent_callback(self, callback_context: CallbackContext) -> Any | None:
        """Handle agent end."""
        try:
            invocation_id = get_invocation_id(callback_context)
            run_id = self._agent_run_ids.pop(invocation_id, None)
            if run_id:
                self._observer.on_agent_end(run_id, callback_context)
        except Exception as e:
            _logger.error(f"Error in after_agent_callback: {e}", exc_info=True)
        return None

    def before_model_callback(self, callback_context: CallbackContext, llm_request: LlmRequest) -> LlmResponse | None:
        """Handle LLM call start."""
        try:
            invocation_id = get_invocation_id(callback_context)
            parent_run_id = self._agent_run_ids.get(invocation_id)
            run_id = self._observer.on_llm_start(callback_context, llm_request, parent_run_id)
            self._llm_run_ids[invocation_id] = run_id
            callback_context._galileo_llm_run_id = run_id  # type: ignore[attr-defined]
        except Exception as e:
            _logger.error(f"Error in before_model_callback: {e}", exc_info=True)
        return None

    def after_model_callback(
        self, callback_context: CallbackContext, llm_response: LlmResponse, model_response_event: Any | None = None
    ) -> LlmResponse | None:
        """Handle LLM call end."""
        try:
            invocation_id = get_invocation_id(callback_context)
            run_id = self._llm_run_ids.pop(invocation_id, None)
            if run_id:
                self._observer.on_llm_end(run_id, llm_response)
        except Exception as e:
            _logger.error(f"Error in after_model_callback: {e}", exc_info=True)
        return None

    def before_tool_callback(
        self, tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
    ) -> dict[str, Any] | None:
        """Handle tool call start."""
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            parent_run_id = self._agent_run_ids.get(invocation_id)
            run_id = self._observer.on_tool_start(tool, args, tool_context, parent_run_id)
            tool_name = getattr(tool, "name", "unknown")
            function_call_id = str(getattr(tool_context, "function_call_id", "none"))
            tool_key = f"{invocation_id}|{tool_name}|{function_call_id}"
            self._tool_run_ids[tool_key] = run_id
            tool_context._galileo_tool_run_id = run_id  # type: ignore[attr-defined]
            tool_context._galileo_tool_key = tool_key  # type: ignore[attr-defined]
        except Exception as e:
            _logger.error(f"Error in before_tool_callback: {e}", exc_info=True)
        return None

    def after_tool_callback(
        self, tool: BaseTool, args: dict[str, Any], tool_context: ToolContext, tool_response: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Handle tool call end."""
        try:
            tool_key = getattr(tool_context, "_galileo_tool_key", None)
            if tool_key:
                run_id = self._tool_run_ids.pop(tool_key, None)
                if run_id:
                    self._observer.on_tool_end(run_id, tool_response)
        except Exception as e:
            _logger.error(f"Error in after_tool_callback: {e}", exc_info=True)
        return None
