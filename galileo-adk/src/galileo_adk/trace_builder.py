"""Lightweight trace builder for ingestion hook mode.

This module provides a TraceBuilder class that implements the same interface as
GalileoLogger for trace building, but without requiring Galileo credentials or
backend connectivity.

When using `ingestion_hook`, the plugin can build traces locally and pass them
to the hook consumer, who handles ingestion (potentially with their own logger
and credentials).
"""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any

from galileo_core.schemas.logging.agent import AgentType
from galileo_core.schemas.logging.span import LlmMetrics, RetrieverSpan, ToolSpan
from galileo_core.schemas.logging.step import Metrics
from galileo_core.schemas.shared.traces_logger import TracesLogger
from pydantic import PrivateAttr

from galileo.schema.logged import LoggedAgentSpan, LoggedLlmSpan, LoggedTrace, LoggedWorkflowSpan
from galileo.schema.trace import TracesIngestRequest
from galileo.utils.retrievers import convert_to_documents

_logger = logging.getLogger(__name__)


def _handle_async_hook_result(task: asyncio.Task) -> None:
    """Log errors from async ingestion hooks."""
    if task.cancelled():
        _logger.warning("TraceBuilder: async ingestion hook was cancelled")
    elif exc := task.exception():
        _logger.error("TraceBuilder: async ingestion hook failed: %s", exc)


MetadataValue = str | bool | int | float | None


class TraceBuilder(TracesLogger):
    """Lightweight trace builder for ingestion hook mode.

    Inherits trace-building logic from TracesLogger (same base as GalileoLogger).
    No Galileo credentials or backend connection required.

    This class provides the same interface as GalileoLogger for:
    - Starting traces and adding spans (llm, tool, workflow, agent, retriever)
    - Managing parent span hierarchy
    - Flushing traces (calls ingestion_hook instead of API)

    Attributes
    ----------
    session_id : str | None
        Session ID (not used in hook mode, but kept for interface compatibility)
    _session_external_id : str | None
        External session ID for correlation (passed to ingestion hook)
    _ingestion_hook : Callable[[TracesIngestRequest], None]
        The hook function to call on flush
    """

    # Public fields (Pydantic fields)
    traces: list[LoggedTrace] = []
    session_id: str | None = None

    # Private attributes (use PrivateAttr for non-field attributes)
    _session_external_id: str | None = PrivateAttr(default=None)
    _ingestion_hook: Callable[[TracesIngestRequest], None] = PrivateAttr()

    def __init__(self, ingestion_hook: Callable[[TracesIngestRequest], None], **data: Any) -> None:
        """Initialize the trace builder.

        Parameters
        ----------
        ingestion_hook : Callable[[TracesIngestRequest], None]
            A callable that receives TracesIngestRequest on flush.
            Can be sync or async.
        """
        super().__init__(**data)
        self._ingestion_hook = ingestion_hook
        self._session_external_id = None

    def add_trace(
        self,
        input: str,
        redacted_input: str | None = None,
        output: str | None = None,
        redacted_output: str | None = None,
        name: str | None = None,
        created_at: datetime | None = None,
        duration_ns: int | None = None,
        user_metadata: dict[str, str] | None = None,
        tags: list[str] | None = None,
        dataset_input: str | None = None,
        dataset_output: str | None = None,
        dataset_metadata: dict[str, str] | None = None,
        external_id: str | None = None,
        id: uuid.UUID | None = None,
    ) -> LoggedTrace:
        if self.current_parent() is not None:
            raise ValueError("You must conclude the existing trace before adding a new one.")
        trace = LoggedTrace(
            input=input,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=created_at,
            user_metadata=user_metadata,
            tags=tags,
            metrics=Metrics(duration_ns=duration_ns),
            dataset_input=dataset_input,
            dataset_output=dataset_output,
            dataset_metadata=dataset_metadata if dataset_metadata is not None else {},
            external_id=external_id,
            id=id,
        )
        trace._parent = None
        self.traces.append(trace)
        self._set_current_parent(trace)
        return trace

    @staticmethod
    def _convert_metadata_value(v: Any) -> str:
        """Convert a metadata value to string."""
        if v is None:
            return "None"
        if isinstance(v, str):
            return v
        return str(v)

    def start_trace(
        self,
        input: str | dict[str, Any],
        redacted_input: str | dict[str, Any] | None = None,
        name: str | None = None,
        duration_ns: int | None = None,
        created_at: datetime | None = None,
        metadata: dict[str, MetadataValue] | None = None,
        tags: list[str] | None = None,
        dataset_input: str | None = None,
        dataset_output: str | None = None,
        dataset_metadata: dict[str, MetadataValue] | None = None,
        external_id: str | None = None,
    ) -> LoggedTrace:
        """Create a new trace and add it to the list of traces.

        This method mirrors GalileoLogger.start_trace() for API compatibility
        with GalileoBaseHandler.

        Parameters
        ----------
        input : str | dict[str, Any]
            Input to the trace. Dicts are auto-converted to JSON strings.
        redacted_input : Optional[str | dict[str, Any]]
            Redacted input (sensitive data removed).
        name : Optional[str]
            Name of the trace.
        duration_ns : Optional[int]
            Duration in nanoseconds.
        created_at : Optional[datetime]
            Timestamp of creation.
        metadata : Optional[dict[str, MetadataValue]]
            Metadata (values auto-converted to strings).
        tags : Optional[list[str]]
            Tags for the trace.
        dataset_input : Optional[str]
            Dataset input.
        dataset_output : Optional[str]
            Dataset expected output.
        dataset_metadata : Optional[dict[str, MetadataValue]]
            Dataset metadata.
        external_id : Optional[str]
            External ID for correlation.

        Returns
        -------
        Trace
            The created trace.
        """
        if isinstance(input, dict):
            input = json.dumps(input)
        if isinstance(redacted_input, dict):
            redacted_input = json.dumps(redacted_input)

        converted_metadata: dict[str, str] | None = None
        if metadata:
            converted_metadata = {k: self._convert_metadata_value(v) for k, v in metadata.items()}

        converted_dataset_metadata: dict[str, str] | None = None
        if dataset_metadata:
            converted_dataset_metadata = {k: self._convert_metadata_value(v) for k, v in dataset_metadata.items()}

        return self.add_trace(
            id=uuid.uuid4(),
            input=input,
            redacted_input=redacted_input,
            name=name,
            duration_ns=duration_ns,
            created_at=created_at,
            user_metadata=converted_metadata,
            tags=tags,
            dataset_input=dataset_input,
            dataset_output=dataset_output,
            dataset_metadata=converted_dataset_metadata,
            external_id=external_id,
        )

    def add_workflow_span(
        self,
        input: str,
        redacted_input: str | None = None,
        output: str | None = None,
        redacted_output: str | None = None,
        name: str | None = None,
        duration_ns: int | None = None,
        created_at: datetime | None = None,
        metadata: dict[str, str] | None = None,
        tags: list[str] | None = None,
        step_number: int | None = None,
        status_code: int | None = None,
    ) -> LoggedWorkflowSpan:
        """Add a workflow span to the current parent.

        This method wraps TracesLogger.add_workflow_span() to accept
        `metadata` parameter (for GalileoBaseHandler compatibility).
        """
        parent = self.current_parent()
        span = LoggedWorkflowSpan(
            input=input,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=self._get_child_span_timestamp() if created_at is None else created_at,
            user_metadata=metadata,
            tags=tags,
            metrics=Metrics(duration_ns=duration_ns),
            id=uuid.uuid4(),
            step_number=step_number,
        )
        span._parent = parent
        self.add_child_span_to_parent(span)
        self._set_current_parent(span)
        if status_code is not None:
            span.status_code = status_code
        return span

    def add_agent_span(
        self,
        input: str,
        redacted_input: str | None = None,
        output: str | None = None,
        redacted_output: str | None = None,
        name: str | None = None,
        duration_ns: int | None = None,
        created_at: datetime | None = None,
        metadata: dict[str, str] | None = None,
        tags: list[str] | None = None,
        agent_type: AgentType | None = None,
        step_number: int | None = None,
        status_code: int | None = None,
    ) -> LoggedAgentSpan:
        """Add an agent span to the current parent.

        This method wraps TracesLogger.add_agent_span() to accept
        `metadata` parameter (for GalileoBaseHandler compatibility).
        """
        parent = self.current_parent()
        span = LoggedAgentSpan(
            input=input,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=self._get_child_span_timestamp() if created_at is None else created_at,
            user_metadata=metadata,
            tags=tags,
            metrics=Metrics(duration_ns=duration_ns),
            agent_type=agent_type,
            id=uuid.uuid4(),
            step_number=step_number,
        )
        span._parent = parent
        self.add_child_span_to_parent(span)
        self._set_current_parent(span)
        if status_code is not None:
            span.status_code = status_code
        return span

    def add_llm_span(
        self,
        input: Any,
        output: Any,
        model: str | None,
        redacted_input: Any | None = None,
        redacted_output: Any | None = None,
        tools: list[dict] | None = None,
        name: str | None = None,
        created_at: datetime | None = None,
        duration_ns: int | None = None,
        metadata: dict[str, str] | None = None,
        tags: list[str] | None = None,
        num_input_tokens: int | None = None,
        num_output_tokens: int | None = None,
        total_tokens: int | None = None,
        temperature: float | None = None,
        status_code: int | None = None,
        time_to_first_token_ns: int | None = None,
        step_number: int | None = None,
        events: list[Any] | None = None,
    ) -> LoggedLlmSpan:
        """Add an LLM span to the current parent.

        This method wraps TracesLogger.add_llm_span() to accept
        `metadata` parameter (for GalileoBaseHandler compatibility).
        """
        span = LoggedLlmSpan(
            input=input,
            output=output,
            model=model,
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            tools=tools,
            name=name,
            created_at=self._get_child_span_timestamp() if created_at is None else created_at,
            user_metadata=metadata,
            tags=tags,
            metrics=LlmMetrics(
                duration_ns=duration_ns,
                num_input_tokens=num_input_tokens,
                num_output_tokens=num_output_tokens,
                num_total_tokens=total_tokens,
                time_to_first_token_ns=time_to_first_token_ns,
            ),
            events=events,
            temperature=temperature,
            status_code=status_code,
            id=uuid.uuid4(),
            step_number=step_number,
        )
        self.add_child_span_to_parent(span)
        return span

    def add_tool_span(
        self,
        input: str,
        redacted_input: str | None = None,
        output: str | None = None,
        redacted_output: str | None = None,
        name: str | None = None,
        duration_ns: int | None = None,
        created_at: datetime | None = None,
        metadata: dict[str, str] | None = None,
        tags: list[str] | None = None,
        status_code: int | None = None,
        tool_call_id: str | None = None,
        step_number: int | None = None,
    ) -> ToolSpan:
        """Add a tool span to the current parent.

        This method wraps TracesLogger.add_tool_span() to accept
        `metadata` parameter (for GalileoBaseHandler compatibility).
        """
        return super().add_tool_span(
            id=uuid.uuid4(),
            input=input,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            duration_ns=duration_ns,
            created_at=created_at,
            user_metadata=metadata,
            tags=tags,
            status_code=status_code,
            tool_call_id=tool_call_id,
            step_number=step_number,
        )

    def add_retriever_span(
        self,
        input: str,
        output: Any,
        redacted_input: str | None = None,
        redacted_output: Any | None = None,
        name: str | None = None,
        duration_ns: int | None = None,
        created_at: datetime | None = None,
        metadata: dict[str, str] | None = None,
        tags: list[str] | None = None,
        status_code: int | None = None,
        step_number: int | None = None,
    ) -> RetrieverSpan:
        """Add a retriever span to the current parent.

        This method wraps TracesLogger.add_retriever_span() to accept
        `metadata` parameter (for GalileoBaseHandler compatibility).
        """
        documents = convert_to_documents(output, "output")
        redacted_documents = convert_to_documents(redacted_output, "redacted_output")
        return super().add_retriever_span(
            id=uuid.uuid4(),
            input=input,
            documents=documents,
            redacted_input=redacted_input,
            redacted_documents=redacted_documents,
            name=name,
            duration_ns=duration_ns,
            created_at=created_at,
            user_metadata=metadata,
            tags=tags,
            status_code=status_code,
            step_number=step_number,
        )

    def flush(self) -> list:
        """Build TracesIngestRequest and pass to ingestion hook.

        Returns
        -------
        list
            Empty list (traces are passed to hook, not returned)
        """
        if not self.traces:
            _logger.debug("TraceBuilder.flush: No traces to flush")
            return []

        request = TracesIngestRequest(
            traces=self.traces,
            session_external_id=self._session_external_id,
        )

        _logger.info("TraceBuilder.flush: Passing %d trace(s) to ingestion_hook", len(self.traces))

        # Handle async hooks
        if inspect.iscoroutinefunction(self._ingestion_hook):
            try:
                loop = asyncio.get_running_loop()
                task = loop.create_task(self._ingestion_hook(request))
                task.add_done_callback(_handle_async_hook_result)
            except RuntimeError:
                asyncio.run(self._ingestion_hook(request))
        else:
            self._ingestion_hook(request)

        # Clear traces after flush
        flushed_traces = self.traces
        self.traces = []
        self._set_current_parent(None)

        return flushed_traces
