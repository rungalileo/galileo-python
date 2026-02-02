"""Shared observability logic for Galileo ADK integration."""

import logging
import uuid
from collections.abc import Callable
from typing import Any
from uuid import UUID

from galileo import galileo_context
from galileo.handlers.base_handler import GalileoBaseHandler
from galileo.logger import GalileoLogger
from galileo.schema.trace import TracesIngestRequest
from galileo.utils.serialization import serialize_to_str
from galileo_adk.data_converters import (
    convert_adk_content_to_galileo_messages,
    convert_adk_tools_to_galileo_format,
    extract_text_from_adk_content,
)
from galileo_adk.span_manager import SpanManager

_logger = logging.getLogger(__name__)


def get_invocation_id(context: Any) -> str:
    """Extract invocation_id from context for correlation."""
    return str(getattr(context, "invocation_id", "unknown"))


def get_tool_invocation_id(tool_context: Any) -> str:
    """Get invocation_id from tool context."""
    if hasattr(tool_context, "invocation_id"):
        return str(tool_context.invocation_id)
    if hasattr(tool_context, "callback_context"):
        return get_invocation_id(tool_context.callback_context)
    return "unknown"


def get_session_id(context: Any) -> str:
    """Extract session_id from context for cross-invocation correlation.

    ADK sessions span multiple invocations, so parent tools and sub-invocations
    share the same session_id even when they have different invocation_ids.
    """
    # Try direct session attribute
    if hasattr(context, "session"):
        session = context.session
        if hasattr(session, "session_id"):
            return str(session.session_id)
    # Try invocation_context path
    if hasattr(context, "_invocation_context"):
        inv_ctx = context._invocation_context
        if hasattr(inv_ctx, "session"):
            session = inv_ctx.session
            if hasattr(session, "session_id"):
                return str(session.session_id)
    return "unknown"


def get_tool_session_id(tool_context: Any) -> str:
    """Get session_id from tool context."""
    if hasattr(tool_context, "session"):
        session = tool_context.session
        if hasattr(session, "session_id"):
            return str(session.session_id)
    if hasattr(tool_context, "callback_context"):
        return get_session_id(tool_context.callback_context)
    return "unknown"


class GalileoObserver:
    """Shared observability logic for Plugin and Callback interfaces."""

    def __init__(
        self,
        project: str | None = None,
        log_stream: str | None = None,
        galileo_logger: GalileoLogger | None = None,
        start_new_trace: bool = True,
        flush_on_completion: bool = True,
        ingestion_hook: Callable[[TracesIngestRequest], None] | None = None,
        external_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if galileo_logger is None:
            if ingestion_hook:
                # Ingestion Hook mode - create logger directly with hook, no credentials needed
                galileo_logger = GalileoLogger(ingestion_hook=ingestion_hook)
            else:
                # Standard mode - use context (requires project/log_stream)
                galileo_logger = galileo_context.get_logger_instance(project=project, log_stream=log_stream)

        if external_id:
            galileo_logger.start_session(name=external_id, external_id=external_id)

        self._handler = GalileoBaseHandler(
            galileo_logger=galileo_logger,
            start_new_trace=start_new_trace,
            flush_on_chain_end=flush_on_completion,
            integration="google_adk",
            ingestion_hook=ingestion_hook,
        )
        self._span_manager = SpanManager(self._handler)
        self._global_metadata = metadata or {}

    @property
    def handler(self) -> GalileoBaseHandler:
        """Access the underlying handler."""
        return self._handler

    def on_run_start(
        self,
        invocation_context: Any,
        user_message: Any,
        parent_run_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> UUID:
        """Handle run start."""
        run_id = uuid.uuid4()
        input_text = extract_text_from_adk_content(user_message)
        combined_metadata = self._extract_invocation_metadata(invocation_context)
        if metadata:
            combined_metadata.update(metadata)
        agent_name = getattr(invocation_context, "agent_name", None) or "agent"
        self._span_manager.start_run(
            run_id=run_id,
            input_data=input_text,
            metadata=combined_metadata,
            agent_name=agent_name,
            parent_run_id=parent_run_id,
        )
        return run_id

    def on_run_end(self, run_id: UUID, output: str, status_code: int = 200) -> None:
        """Handle run end."""
        self._span_manager.end_run(run_id=run_id, output=output, status_code=status_code)

    def on_event(self, run_id: UUID, event: Any) -> None:
        """Handle streaming event."""
        pass

    def on_agent_start(
        self, callback_context: Any, parent_run_id: UUID | None = None, metadata: dict[str, Any] | None = None
    ) -> UUID:
        """Handle agent start."""
        run_id = uuid.uuid4()
        agent_name = getattr(callback_context, "agent_name", "Agent")
        input_text = self._extract_agent_input(callback_context)
        combined_metadata = self._extract_agent_metadata(callback_context)
        if metadata:
            combined_metadata.update(metadata)
        self._span_manager.start_agent(
            run_id=run_id,
            parent_run_id=parent_run_id,
            input_data=input_text,
            name=agent_name,
            metadata=combined_metadata,
        )
        return run_id

    def on_agent_end(self, run_id: UUID, callback_context: Any, status_code: int = 200) -> None:
        """Handle agent end."""
        output = self._extract_agent_output(callback_context)
        self._span_manager.end_agent(run_id=run_id, output=output, status_code=status_code)

    def on_llm_start(
        self,
        callback_context: Any,
        llm_request: Any,
        parent_run_id: UUID | None,
        metadata: dict[str, Any] | None = None,
    ) -> UUID:
        """Handle LLM call start."""
        run_id = uuid.uuid4()
        input_messages = self._extract_llm_input(llm_request)
        model = self._extract_model_name(llm_request)
        temperature = self._extract_temperature(llm_request)
        tools = self._extract_tools(llm_request)
        combined_metadata = {**self._global_metadata, **(metadata or {})}
        self._span_manager.start_llm(
            run_id=run_id,
            parent_run_id=parent_run_id,
            input_data=input_messages,
            model=model,
            temperature=temperature,
            tools=tools,
            metadata=combined_metadata,
        )
        return run_id

    def on_llm_end(self, run_id: UUID, llm_response: Any, status_code: int = 200) -> None:
        """Handle LLM call end."""
        output = self._extract_llm_output(llm_response)
        usage = self._extract_usage_metadata(llm_response)
        self._span_manager.end_llm(
            run_id=run_id,
            output=output,
            num_input_tokens=usage.get("prompt_tokens"),
            num_output_tokens=usage.get("completion_tokens"),
            total_tokens=usage.get("total_tokens"),
            status_code=status_code,
        )

    def on_tool_start(
        self,
        tool: Any,
        tool_args: dict[str, Any],
        tool_context: Any,
        parent_run_id: UUID | None,
        metadata: dict[str, Any] | None = None,
    ) -> UUID:
        """Handle tool call start."""
        run_id = uuid.uuid4()
        tool_name = getattr(tool, "name", "unknown_tool")
        combined_metadata = {**self._global_metadata, **(metadata or {})}
        self._span_manager.start_tool(
            run_id=run_id,
            parent_run_id=parent_run_id,
            input_data=serialize_to_str(tool_args),
            name=tool_name,
            metadata=combined_metadata,
        )
        return run_id

    def on_tool_end(self, run_id: UUID, result: Any, status_code: int = 200) -> None:
        """Handle tool call end."""
        self._span_manager.end_tool(run_id=run_id, output=serialize_to_str(result), status_code=status_code)

    def _extract_invocation_metadata(self, invocation_context: Any) -> dict[str, Any]:
        metadata = {**self._global_metadata}
        if hasattr(invocation_context, "invocation_id"):
            metadata["invocation_id"] = str(invocation_context.invocation_id)
        if hasattr(invocation_context, "session"):
            session = invocation_context.session
            if hasattr(session, "session_id"):
                metadata["session_id"] = str(session.session_id)
        return metadata

    def _extract_agent_input(self, callback_context: Any) -> str:
        if hasattr(callback_context, "parent_context"):
            parent = callback_context.parent_context
            if hasattr(parent, "new_message"):
                return extract_text_from_adk_content(parent.new_message)
        return "Agent invocation"

    def _extract_agent_output(self, callback_context: Any) -> str:
        if hasattr(callback_context, "parent_context"):
            parent = callback_context.parent_context
            if hasattr(parent, "events") and parent.events:
                last_event = parent.events[-1] if isinstance(parent.events, list) else None
                if last_event and hasattr(last_event, "content"):
                    return extract_text_from_adk_content(last_event.content)
        return ""

    def _extract_agent_metadata(self, callback_context: Any) -> dict[str, Any]:
        return {
            **self._global_metadata,
            "agent_name": getattr(callback_context, "agent_name", None),
        }

    def _extract_llm_input(self, llm_request: Any) -> list[Any]:
        if not hasattr(llm_request, "contents"):
            return []
        messages = []
        for content in llm_request.contents:
            messages.extend(convert_adk_content_to_galileo_messages(content))
        return messages

    def _extract_llm_output(self, llm_response: Any) -> list[Any]:
        """Extract LLM output as list of Messages to preserve all parts including tool_calls."""
        if llm_response and hasattr(llm_response, "content"):
            return convert_adk_content_to_galileo_messages(llm_response.content)
        return []

    def _extract_model_name(self, llm_request: Any) -> str | None:
        return str(llm_request.model) if hasattr(llm_request, "model") else None

    def _extract_temperature(self, llm_request: Any) -> float | None:
        if hasattr(llm_request, "config") and llm_request.config:
            temp = getattr(llm_request.config, "temperature", None)
            if temp is not None:
                try:
                    return float(temp)
                except (ValueError, TypeError):
                    pass
        return None

    def _extract_tools(self, llm_request: Any) -> list[dict[str, Any]] | None:
        if hasattr(llm_request, "config") and llm_request.config:
            tools = getattr(llm_request.config, "tools", None)
            if tools:
                return convert_adk_tools_to_galileo_format(tools)
        return None

    def _extract_usage_metadata(self, llm_response: Any) -> dict[str, Any]:
        """Extract token usage metrics from LLM response."""
        if not llm_response:
            return {}
        usage = getattr(llm_response, "usage_metadata", None)
        if not usage:
            return {}
        return {
            "prompt_tokens": getattr(usage, "prompt_token_count", None),
            "completion_tokens": getattr(usage, "candidates_token_count", None),
            "total_tokens": getattr(usage, "total_token_count", None),
        }

    def _extract_final_output(self, invocation_context: Any) -> str:
        if hasattr(invocation_context, "session"):
            session = invocation_context.session
            if hasattr(session, "events") and session.events:
                last_event = session.events[-1] if isinstance(session.events, list) else None
                if last_event and hasattr(last_event, "content"):
                    return extract_text_from_adk_content(last_event.content)
        return ""
