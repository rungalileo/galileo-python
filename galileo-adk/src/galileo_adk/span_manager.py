"""Span hierarchy management for Galileo ADK."""

import time
from typing import Any
from uuid import UUID

from galileo.handlers.base_handler import GalileoBaseHandler
from galileo_adk.types import EventData, RunContext

# Integration tag for all spans
INTEGRATION_TAG = "google_adk"


class SpanManager:
    """Manages span creation and hierarchy for Galileo observability."""

    def __init__(self, handler: GalileoBaseHandler) -> None:
        self._handler = handler
        self._run_contexts: dict[str, RunContext] = {}

    def start_run(self, run_id: UUID, input_data: str, metadata: dict[str, Any] | None = None) -> None:
        """Start a run span (root of trace hierarchy)."""
        self._handler.start_node(
            node_type="workflow",
            parent_run_id=None,
            run_id=run_id,
            input=input_data,
            name="ADK Run",
            tags=[INTEGRATION_TAG, "run"],
            metadata=metadata,
        )
        self._run_contexts[str(run_id)] = RunContext(
            run_id=run_id,
            start_time_ns=time.time_ns(),
            metadata=metadata or {},
        )

    def end_run(self, run_id: UUID, output: str) -> None:
        """End a run span."""
        context = self._run_contexts.pop(str(run_id), None)
        events_count = len(context.events) if context else 0
        self._handler.end_node(run_id=run_id, output=output, metadata={"events_count": events_count})

    def record_event(self, run_id: UUID, event_data: EventData) -> None:
        """Record a streaming event on the run."""
        context = self._run_contexts.get(str(run_id))
        if context:
            context.events.append(event_data)

    def start_agent(
        self,
        run_id: UUID,
        parent_run_id: UUID | None,
        input_data: str,
        name: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Start an agent span."""
        self._handler.start_node(
            node_type="agent",
            parent_run_id=parent_run_id,
            run_id=run_id,
            input=input_data,
            name=name,
            tags=[INTEGRATION_TAG, f"agent:{name}"],
            metadata=metadata,
        )

    def end_agent(self, run_id: UUID, output: str) -> None:
        """End an agent span."""
        self._handler.end_node(run_id=run_id, output=output)

    def start_llm(
        self,
        run_id: UUID,
        parent_run_id: UUID | None,
        input_data: Any,
        model: str | None = None,
        temperature: float | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> None:
        """Start an LLM span."""
        self._handler.start_node(
            node_type="llm",
            parent_run_id=parent_run_id,
            run_id=run_id,
            input=input_data,
            model=model,
            temperature=temperature,
            tools=tools,
            tags=[INTEGRATION_TAG, "llm"],
        )

    def end_llm(
        self,
        run_id: UUID,
        output: Any,
        num_input_tokens: int | None = None,
        num_output_tokens: int | None = None,
        total_tokens: int | None = None,
    ) -> None:
        """End an LLM span."""
        self._handler.end_node(
            run_id=run_id,
            output=output,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            total_tokens=total_tokens,
        )

    def start_tool(self, run_id: UUID, parent_run_id: UUID | None, input_data: str, name: str) -> None:
        """Start a tool span."""
        self._handler.start_node(
            node_type="tool",
            parent_run_id=parent_run_id,
            run_id=run_id,
            input=input_data,
            name=name,
            tags=[INTEGRATION_TAG, "tool", f"tool:{name}"],
        )

    def end_tool(self, run_id: UUID, output: str) -> None:
        """End a tool span."""
        self._handler.end_node(run_id=run_id, output=output)
