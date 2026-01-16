"""Galileo ADK Plugin - Runner-level observability for Google ADK."""

import logging
import uuid
from collections.abc import Callable
from typing import Any
from uuid import UUID

from galileo.logger import GalileoLogger
from galileo.schema.trace import TracesIngestRequest
from galileo_adk.observer import GalileoObserver, get_invocation_id, get_tool_invocation_id

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


class GalileoADKPlugin(BasePlugin):
    """Galileo observability plugin for Google ADK Runner."""

    def __init__(
        self,
        project: str | None = None,
        log_stream: str | None = None,
        galileo_logger: GalileoLogger | None = None,
        start_new_trace: bool = True,
        flush_on_run_end: bool = True,
        ingestion_hook: Callable[[TracesIngestRequest], None] | None = None,
    ) -> None:
        super().__init__(name="galileo")
        self._observer = GalileoObserver(
            project=project,
            log_stream=log_stream,
            galileo_logger=galileo_logger,
            start_new_trace=start_new_trace,
            flush_on_completion=flush_on_run_end,
            ingestion_hook=ingestion_hook,
        )
        self._run_ids: dict[str, UUID] = {}
        self._agent_run_ids: dict[str, UUID] = {}
        self._llm_run_ids: dict[str, UUID] = {}
        self._tool_run_ids: dict[str, UUID] = {}

    async def on_user_message_callback(
        self, *, invocation_context: InvocationContext, user_message: Content
    ) -> Content | None:
        """Capture user message and start run span."""
        try:
            run_id = self._observer.on_run_start(invocation_context, user_message)
            invocation_id = get_invocation_id(invocation_context)
            self._run_ids[invocation_id] = run_id
            invocation_context._galileo_run_id = run_id  # type: ignore[attr-defined]
        except Exception as e:
            _logger.error(f"Error in on_user_message_callback: {e}", exc_info=True)
        return None

    async def before_run_callback(self, *, invocation_context: InvocationContext) -> None:
        """Called before agent processing starts."""
        pass

    async def after_run_callback(self, *, invocation_context: InvocationContext) -> None:
        """Finalize run span."""
        try:
            invocation_id = get_invocation_id(invocation_context)
            run_id = self._run_ids.pop(invocation_id, None)
            if run_id:
                output = self._observer._extract_final_output(invocation_context)
                self._observer.on_run_end(run_id=run_id, output=output)
        except Exception as e:
            _logger.error(f"Error in after_run_callback: {e}", exc_info=True)

    async def before_agent_callback(self, *, callback_context: CallbackContext, **kwargs: Any) -> Content | None:
        """Handle agent start."""
        try:
            invocation_id = get_invocation_id(callback_context)
            parent_run_id = self._run_ids.get(invocation_id)
            run_id = self._observer.on_agent_start(callback_context, parent_run_id)
            self._agent_run_ids[invocation_id] = run_id
            callback_context._galileo_run_id = run_id  # type: ignore[attr-defined]
        except Exception as e:
            _logger.error(f"Error in before_agent_callback: {e}", exc_info=True)
        return None

    async def after_agent_callback(self, *, callback_context: CallbackContext, **kwargs: Any) -> Content | None:
        """Handle agent end."""
        try:
            invocation_id = get_invocation_id(callback_context)
            run_id = self._agent_run_ids.pop(invocation_id, None)
            if run_id:
                self._observer.on_agent_end(run_id, callback_context)
        except Exception as e:
            _logger.error(f"Error in after_agent_callback: {e}", exc_info=True)
        return None

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> LlmResponse | None:
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

    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse
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

    async def on_model_error_callback(
        self, *, callback_context: CallbackContext, error: Exception
    ) -> LlmResponse | None:
        """Capture LLM errors."""
        try:
            invocation_id = get_invocation_id(callback_context)
            run_id = self._llm_run_ids.pop(invocation_id, None)
            if run_id:
                self._observer.on_llm_end(run_id, None)
        except Exception as e:
            _logger.error(f"Error in on_model_error_callback: {e}", exc_info=True)
        return None

    async def before_tool_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext
    ) -> dict[str, Any] | None:
        """Handle tool call start."""
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            parent_run_id = self._agent_run_ids.get(invocation_id)
            run_id = self._observer.on_tool_start(tool, tool_args, tool_context, parent_run_id)
            tool_name = getattr(tool, "name", "unknown")
            call_id = getattr(tool_context, "function_call_id", None) or str(uuid.uuid4())
            tool_key = f"{invocation_id}|{tool_name}|{call_id}"
            self._tool_run_ids[tool_key] = run_id
            tool_context._galileo_tool_run_id = run_id  # type: ignore[attr-defined]
            tool_context._galileo_tool_key = tool_key  # type: ignore[attr-defined]
        except Exception as e:
            _logger.error(f"Error in before_tool_callback: {e}", exc_info=True)
        return None

    async def after_tool_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext, result: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Handle tool call end."""
        try:
            tool_key = getattr(tool_context, "_galileo_tool_key", None)
            if tool_key:
                run_id = self._tool_run_ids.pop(tool_key, None)
                if run_id:
                    self._observer.on_tool_end(run_id, result)
        except Exception as e:
            _logger.error(f"Error in after_tool_callback: {e}", exc_info=True)
        return None

    async def on_tool_error_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext, error: Exception
    ) -> dict[str, Any] | None:
        """Capture tool errors."""
        try:
            tool_key = getattr(tool_context, "_galileo_tool_key", None)
            if tool_key:
                run_id = self._tool_run_ids.pop(tool_key, None)
                if run_id:
                    self._observer.on_tool_end(run_id, {"error": str(error)})
        except Exception as e:
            _logger.error(f"Error in on_tool_error_callback: {e}", exc_info=True)
        return None

    async def on_event_callback(self, *, invocation_context: InvocationContext, event: Event) -> Event | None:
        """Capture streaming events."""
        try:
            invocation_id = get_invocation_id(invocation_context)
            run_id = self._run_ids.get(invocation_id)
            if run_id:
                self._observer.on_event(run_id, event)
        except Exception as e:
            _logger.error(f"Error in on_event_callback: {e}", exc_info=True)
        return None
