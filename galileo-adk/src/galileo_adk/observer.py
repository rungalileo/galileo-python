"""Shared observability logic for Galileo ADK integration."""

from __future__ import annotations

import contextlib
import logging
import uuid
import weakref
from collections.abc import Callable
from typing import Any
from uuid import UUID

from galileo import galileo_context
from galileo.handlers.base_handler import GalileoBaseHandler
from galileo.schema.trace import TracesIngestRequest
from galileo.utils.serialization import serialize_to_str
from galileo_adk.data_converters import (
    convert_adk_content_to_galileo_messages,
    convert_adk_tools_to_galileo_format,
    extract_text_from_adk_content,
)
from galileo_adk.span_manager import SpanManager
from galileo_adk.trace_builder import TraceBuilder

_logger = logging.getLogger(__name__)

# Cache generated invocation IDs without mutating ADK objects.
_generated_invocation_ids: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()


def get_invocation_id(context: Any) -> str:
    """Extract invocation_id from context for correlation."""
    invocation_id = getattr(context, "invocation_id", None)
    if invocation_id is not None:
        return str(invocation_id)

    cached = _generated_invocation_ids.get(context)
    if cached is not None:
        return cached

    session_id = get_session_id(context)
    fallback_id = f"{session_id}_{uuid.uuid4()}" if session_id != "unknown" else str(uuid.uuid4())

    with contextlib.suppress(TypeError):
        _generated_invocation_ids[context] = fallback_id

    return fallback_id


def get_tool_invocation_id(tool_context: Any) -> str:
    """Get invocation_id from tool context."""
    if hasattr(tool_context, "invocation_id"):
        return str(tool_context.invocation_id)
    if hasattr(tool_context, "callback_context"):
        return get_invocation_id(tool_context.callback_context)
    return get_invocation_id(tool_context)


def get_session_id(context: Any) -> str:
    """Extract session_id from context for cross-invocation correlation.

    ADK sessions span multiple invocations, so parent tools and sub-invocations
    share the same session_id even when they have different invocation_ids.
    """
    # Try direct session attribute
    if hasattr(context, "session"):
        session = context.session
        if hasattr(session, "id"):
            return str(session.id)
    # Try invocation_context path
    if hasattr(context, "_invocation_context"):
        inv_ctx = context._invocation_context
        if hasattr(inv_ctx, "session"):
            session = inv_ctx.session
            if hasattr(session, "id"):
                return str(session.id)
    return "unknown"


def get_tool_session_id(tool_context: Any) -> str:
    """Get session_id from tool context."""
    if hasattr(tool_context, "session"):
        session = tool_context.session
        if hasattr(session, "id"):
            return str(session.id)
    if hasattr(tool_context, "callback_context"):
        return get_session_id(tool_context.callback_context)
    return "unknown"


def get_agent_name_from_tool_context(tool_context: Any) -> str | None:
    """Extract agent name from tool context."""
    try:
        if hasattr(tool_context, "callback_context"):
            return getattr(tool_context.callback_context, "agent_name", None)
        if hasattr(tool_context, "agent_name"):
            return getattr(tool_context, "agent_name", None)
    except Exception:
        pass
    return None


def get_custom_metadata(context: Any) -> dict[str, Any]:
    """Extract custom_metadata from context's RunConfig.

    Works with both:
    - InvocationContext (Plugin callbacks)
    - CallbackContext (Callback callbacks) - has run_config via ReadonlyContext

    Parameters
    ----------
    context : Any
        ADK context object (InvocationContext or CallbackContext)

    Returns
    -------
    dict[str, Any]
        Custom metadata from RunConfig, or empty dict if not available
    """
    try:
        run_config = getattr(context, "run_config", None)
        if run_config and hasattr(run_config, "custom_metadata") and run_config.custom_metadata:
            return dict(run_config.custom_metadata)
    except Exception:
        pass
    return {}


class GalileoObserver:
    """Shared observability logic for Plugin and Callback interfaces."""

    _trace_builder: TraceBuilder | None

    def __init__(
        self,
        project: str | None = None,
        log_stream: str | None = None,
        ingestion_hook: Callable[[TracesIngestRequest], None] | None = None,
    ) -> None:
        self._current_adk_session: str | None = None

        if ingestion_hook:
            trace_builder = TraceBuilder(ingestion_hook=ingestion_hook)
            self._trace_builder = trace_builder
            self._handler = GalileoBaseHandler(
                galileo_logger=trace_builder,  # type: ignore[arg-type]
                start_new_trace=True,
                flush_on_chain_end=True,
                integration="google_adk",
            )
        else:
            self._trace_builder = None
            galileo_logger = galileo_context.get_logger_instance(project=project, log_stream=log_stream)
            self._handler = GalileoBaseHandler(
                galileo_logger=galileo_logger,
                start_new_trace=True,
                flush_on_chain_end=True,
                integration="google_adk",
            )

        self._span_manager = SpanManager(self._handler)

        # Per-invocation metadata tracking
        self._invocation_metadata: dict[str, dict[str, Any]] = {}
        self._session_root_invocation: dict[str, str] = {}

    @property
    def handler(self) -> GalileoBaseHandler:
        """Access the underlying handler."""
        return self._handler

    @property
    def current_adk_session(self) -> str | None:
        """The currently tracked ADK session ID."""
        return self._current_adk_session

    def force_end_tool(self, run_id: UUID, output: str, status_code: int) -> None:
        """Force-close a tool span (for orphaned span cleanup)."""
        self._span_manager.end_tool(run_id=run_id, output=output, status_code=status_code)

    def force_end_llm(self, run_id: UUID, output: Any, status_code: int) -> None:
        """Force-close an LLM span (for orphaned span cleanup)."""
        self._span_manager.end_llm(run_id=run_id, output=output, status_code=status_code)

    def force_end_agent(self, run_id: UUID, output: str, status_code: int) -> None:
        """Force-close an agent span (for orphaned span cleanup)."""
        self._span_manager.end_agent(run_id=run_id, output=output, status_code=status_code)

    def force_end_run(self, run_id: UUID, output: str, status_code: int) -> None:
        """Force-close a run span (for partial trace commit)."""
        self._span_manager.end_run(run_id=run_id, output=output, status_code=status_code)

    def store_invocation_metadata(self, invocation_id: str, session_id: str, metadata: dict[str, Any]) -> None:
        """Store metadata for an invocation and track as root for the session.

        Parameters
        ----------
        invocation_id : str
            The invocation ID to store metadata for
        session_id : str
            The session ID (used to track root invocation)
        metadata : dict[str, Any]
            The metadata from RunConfig.custom_metadata
        """
        self._invocation_metadata[invocation_id] = metadata

        # Track as root only if metadata is non-empty (sub-invocations have empty metadata)
        if metadata:
            root_session = self._current_adk_session or session_id
            self._session_root_invocation[root_session] = invocation_id

    def get_invocation_metadata(self, invocation_id: str, session_id: str) -> dict[str, Any]:
        """Get metadata for an invocation, falling back to root invocation's metadata.

        Sub-invocations (e.g., AgentTool calls) may have different invocation_ids
        but should inherit metadata from the root invocation.

        Parameters
        ----------
        invocation_id : str
            The invocation ID to get metadata for
        session_id : str
            The session ID (used to find root invocation for fallback)

        Returns
        -------
        dict[str, Any]
            The metadata for the invocation, or empty dict if not found
        """
        metadata = self._invocation_metadata.get(invocation_id)
        if metadata:
            return metadata

        root_session = self._current_adk_session or session_id
        root_invocation_id = self._session_root_invocation.get(root_session)
        if root_invocation_id:
            return self._invocation_metadata.get(root_invocation_id, {})

        return {}

    def cleanup_invocation_metadata(self, invocation_id: str) -> None:
        """Clean up metadata for an invocation after it ends.

        Parameters
        ----------
        invocation_id : str
            The invocation ID to clean up
        """
        self._invocation_metadata.pop(invocation_id, None)

    def update_session_if_changed(self, adk_session_id: str, is_sub_invocation: bool = False) -> None:
        """Map ADK session_id to Galileo session for trace grouping.

        Updates the Galileo session when the ADK session changes. Sessions are linked
        via previous_session_id when switching to maintain continuity.

        In hook mode, session lifecycle is delegated to the hook consumer; only the
        external_id is stored for correlation.

        Parameters
        ----------
        adk_session_id : str
            The ADK session ID from the invocation context
        is_sub_invocation : bool
            If True, this is an AgentTool sub-invocation with a different session_id.
            Sub-invocations should NOT trigger session switching because they are
            spawned by AgentTool within an existing conversation, not user-initiated
            new conversations via runner.run_async().
        """
        if adk_session_id == "unknown":
            return

        # Sub-invocations keep the parent's session for trace coherence
        if self._current_adk_session is not None and is_sub_invocation:
            return

        if adk_session_id == self._current_adk_session:
            return

        self._current_adk_session = adk_session_id

        # Hook mode: store external_id; session creation is the hook consumer's responsibility
        if self._trace_builder is not None:
            self._trace_builder._session_external_id = adk_session_id
            return

        # Normal mode: create/find session on backend
        logger = self._handler._galileo_logger
        previous_session_id = logger.session_id
        logger.start_session(
            name=adk_session_id,
            external_id=adk_session_id,
            previous_session_id=previous_session_id,
        )

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
        combined_metadata = metadata or {}
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
        combined_metadata = metadata or {}
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
        metadata: dict[str, Any] = {}
        if hasattr(invocation_context, "invocation_id"):
            metadata["invocation_id"] = str(invocation_context.invocation_id)
        if hasattr(invocation_context, "session"):
            session = invocation_context.session
            if hasattr(session, "id"):
                metadata["session_id"] = str(session.id)
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
        metadata: dict[str, Any] = {}
        agent_name = getattr(callback_context, "agent_name", None)
        if agent_name is not None:
            metadata["agent_name"] = agent_name
        return metadata

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
            "prompt_tokens": getattr(usage, "prompt_token_count", None) or getattr(usage, "input_token_count", None),
            "completion_tokens": getattr(usage, "candidates_token_count", None)
            or getattr(usage, "output_token_count", None),
            "total_tokens": getattr(usage, "total_token_count", None),
        }

    def _extract_final_output(self, invocation_context: Any) -> str:
        if hasattr(invocation_context, "session"):
            session = invocation_context.session
            if hasattr(session, "events") and session.events and isinstance(session.events, list):
                for event in reversed(session.events):
                    if hasattr(event, "is_final_response") and event.is_final_response() and hasattr(event, "content"):
                        return extract_text_from_adk_content(event.content)
        return ""
