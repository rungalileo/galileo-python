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


def _is_http_status_code(code: int) -> bool:
    """Check if code is a valid HTTP status code (100-599)."""
    return 100 <= code <= 599


def _extract_status_code(error: Exception) -> int:
    """Extract HTTP status code from exception, defaulting to 500.

    Google GenAI/ADK errors may have:
    - code attribute (int or enum with .value) - but may be gRPC code (0-16), not HTTP
    - status_code attribute
    - Code embedded in error message (e.g., "429 RESOURCE_EXHAUSTED")

    Note: gRPC uses different codes (e.g., RESOURCE_EXHAUSTED=8), so we must
    validate that codes are in the HTTP range (100-599) before using them.
    """
    import re

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
    """Galileo observability plugin for Google ADK Runner."""

    def __init__(
        self,
        project: str | None = None,
        log_stream: str | None = None,
        galileo_logger: GalileoLogger | None = None,
        start_new_trace: bool = True,
        flush_on_run_end: bool = True,
        ingestion_hook: Callable[[TracesIngestRequest], None] | None = None,
        external_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(name="galileo")
        self._observer = GalileoObserver(
            project=project,
            log_stream=log_stream,
            galileo_logger=galileo_logger,
            start_new_trace=start_new_trace,
            flush_on_completion=flush_on_run_end,
            ingestion_hook=ingestion_hook,
            external_id=external_id,
            metadata=metadata,
        )
        self._run_ids: dict[str, UUID] = {}
        self._agent_run_ids: dict[str, UUID] = {}
        self._llm_run_ids: dict[str, UUID] = {}
        self._tool_run_ids: dict[str, UUID] = {}
        # Track the most recent active tool - used as parent for tool-invoked agent invocations
        self._last_tool_run_id: UUID | None = None

    def _get_agent_key(self, callback_context: CallbackContext) -> str:
        """Create unique key for agent using invocation_id and agent_name.

        This ensures each agent has its own entry, even when multiple agents
        share the same invocation_id.
        """
        invocation_id = get_invocation_id(callback_context)
        agent_name = getattr(callback_context, "agent_name", "unknown")
        return f"{invocation_id}|{agent_name}"

    def _get_parent_agent_run_id(self, callback_context: CallbackContext) -> UUID | None:
        """Get the run_id of the parent agent, or fall back to root invocation.

        This enables proper nested hierarchy where sub-agents are children of
        their parent agents, not siblings.

        Note: ADK creates NEW invocations for sub-agents during transfer, so we need
        to search for parent agents across ALL invocations, not just the current one.
        """
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
                            # First try same invocation
                            parent_key = f"{invocation_id}|{parent_name}"
                            parent_run_id = self._agent_run_ids.get(parent_key)
                            if parent_run_id:
                                return parent_run_id

                            # Search across ALL invocations for the parent agent
                            # (ADK creates new invocations for sub-agents during transfer)
                            for key, run_id in self._agent_run_ids.items():
                                if key.endswith(f"|{parent_name}"):
                                    return run_id
                    # No parent_agent - agent is root of its invocation, parent is the invocation span
        except Exception as e:
            _logger.debug(f"Exception getting parent: {e}")

        # Fall back to root invocation run
        return self._run_ids.get(invocation_id)

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
        """Capture user message and start run span (invocation wrapper).

        For tool-invoked agents, the invocation span is nested under the tool
        that triggered it (e.g., execute_tool [record_worker] → invocation [record_worker]).
        """
        try:
            # Use last active tool as parent for tool-invoked agent invocations
            parent_run_id = self._last_tool_run_id
            run_id = self._observer.on_run_start(invocation_context, user_message, parent_run_id)
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
            agent_key = self._get_agent_key(callback_context)
            parent_run_id = self._get_parent_agent_run_id(callback_context)
            run_id = self._observer.on_agent_start(callback_context, parent_run_id)
            self._agent_run_ids[agent_key] = run_id
            callback_context._galileo_run_id = run_id  # type: ignore[attr-defined]
        except Exception as e:
            _logger.error(f"Error in before_agent_callback: {e}", exc_info=True)
        return None

    async def after_agent_callback(self, *, callback_context: CallbackContext, **kwargs: Any) -> Content | None:
        """Handle agent end."""
        try:
            agent_key = self._get_agent_key(callback_context)
            run_id = self._agent_run_ids.pop(agent_key, None)
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
            # Use agent-specific key to get current agent's run_id as parent
            agent_key = self._get_agent_key(callback_context)
            parent_run_id = self._agent_run_ids.get(agent_key)
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
        self, *, callback_context: CallbackContext, llm_request: LlmRequest, error: Exception
    ) -> LlmResponse | None:
        """Capture LLM errors."""
        try:
            invocation_id = get_invocation_id(callback_context)
            run_id = self._llm_run_ids.pop(invocation_id, None)
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
        # 429 (rate limit), 401 (auth), 403 (forbidden) are fatal
        return code in (401, 403, 429)

    def _force_commit_partial_trace(self, invocation_id: str, error: Exception) -> None:
        """End all open spans and commit partial trace on fatal error."""
        error_output = f"Error: {error}"
        status_code = _extract_status_code(error)

        # End any open agent spans for this invocation
        for key in list(self._agent_run_ids.keys()):
            if key.startswith(f"{invocation_id}|"):
                agent_run_id = self._agent_run_ids.pop(key)
                self._observer._span_manager.end_agent(
                    run_id=agent_run_id, output=error_output, status_code=status_code
                )

        # End the run span (this triggers commit)
        run_id = self._run_ids.pop(invocation_id, None)
        if run_id:
            self._observer._span_manager.end_run(run_id=run_id, output=error_output, status_code=status_code)

    async def before_tool_callback(
        self, *, tool: BaseTool, tool_args: dict[str, Any], tool_context: ToolContext
    ) -> dict[str, Any] | None:
        """Handle tool call start."""
        try:
            invocation_id = get_tool_invocation_id(tool_context)
            agent_name = self._get_current_agent_name_from_tool_context(tool_context)
            parent_run_id = None
            if agent_name:
                # First try same invocation
                agent_key = f"{invocation_id}|{agent_name}"
                parent_run_id = self._agent_run_ids.get(agent_key)
                # Search across all invocations if not found
                if not parent_run_id:
                    for key, run_id in self._agent_run_ids.items():
                        if key.endswith(f"|{agent_name}"):
                            parent_run_id = run_id
                            break
            run_id = self._observer.on_tool_start(tool, tool_args, tool_context, parent_run_id)
            tool_name = getattr(tool, "name", "unknown")
            call_id = getattr(tool_context, "function_call_id", None) or str(uuid.uuid4())
            tool_key = f"{invocation_id}|{tool_name}|{call_id}"
            self._tool_run_ids[tool_key] = run_id
            self._last_tool_run_id = run_id  # Track for tool-invoked agent invocations
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
        """Capture tool errors.

        Returns the error as a dict so ADK treats it as a tool response rather than
        re-raising the exception. This ensures the run completes and traces are flushed.
        """
        error_response = {"error": str(error)}
        try:
            tool_key = getattr(tool_context, "_galileo_tool_key", None)
            if tool_key:
                run_id = self._tool_run_ids.pop(tool_key, None)
                if run_id:
                    status_code = _extract_status_code(error)
                    self._observer.on_tool_end(run_id, error_response, status_code=status_code)
        except Exception as e:
            _logger.error(f"Error in on_tool_error_callback: {e}", exc_info=True)
        return error_response

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
