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

    def start_run(
        self,
        run_id: UUID,
        input_data: str,
        metadata: dict[str, Any] | None = None,
        agent_name: str = "agent",
        parent_run_id: UUID | None = None,
    ) -> None:
        """Start a run span (invocation wrapper).

        Args:
            run_id: Unique ID for this invocation
            input_data: User input text
            metadata: Additional metadata
            agent_name: Name of the root agent for this invocation
            parent_run_id: Parent span ID (for sub-agent invocations triggered by tools)
        """
        self._handler.start_node(
            node_type="chain",
            parent_run_id=parent_run_id,
            run_id=run_id,
            input=input_data,
            name=f"invocation [{agent_name}]",
            tags=[INTEGRATION_TAG, "invocation"],
            metadata=metadata,
        )
        self._run_contexts[str(run_id)] = RunContext(
            run_id=run_id,
            start_time_ns=time.time_ns(),
            metadata=metadata or {},
        )

    def end_run(self, run_id: UUID, output: str, status_code: int = 200) -> None:
        """End a run span."""
        context = self._run_contexts.pop(str(run_id), None)
        events_count = len(context.events) if context else 0
        self._handler.end_node(
            run_id=run_id, output=output, metadata={"events_count": events_count}, status_code=status_code
        )

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
            name=f"agent_run [{name}]",
            tags=[INTEGRATION_TAG, f"agent:{name}"],
            metadata=metadata,
        )

    def end_agent(self, run_id: UUID, output: str, status_code: int = 200) -> None:
        """End an agent span."""
        self._handler.end_node(run_id=run_id, output=output, status_code=status_code)

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
            name="call_llm",
            model=model,
            temperature=temperature,
            tools=tools,
            tags=[INTEGRATION_TAG, "llm"],
        )

    def end_llm(
        self,
        run_id: UUID,
        output: list[Any] | Any,
        num_input_tokens: int | None = None,
        num_output_tokens: int | None = None,
        total_tokens: int | None = None,
        status_code: int = 200,
    ) -> None:
        """End an LLM span.

        Args:
            run_id: The unique run ID for this span
            output: LLM output - can be a list of Messages (preserves tool_calls)
                   or a single value for backward compatibility
            num_input_tokens: Number of input tokens used
            num_output_tokens: Number of output tokens generated
            total_tokens: Total tokens used
            status_code: HTTP status code (200 for success)
        """
        # Normalize output: empty list becomes None
        normalized_output = None if isinstance(output, list) and not output else output

        self._handler.end_node(
            run_id=run_id,
            output=normalized_output,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            total_tokens=total_tokens,
            status_code=status_code,
        )

    def start_tool(self, run_id: UUID, parent_run_id: UUID | None, input_data: str, name: str) -> None:
        """Start a tool span."""
        self._handler.start_node(
            node_type="tool",
            parent_run_id=parent_run_id,
            run_id=run_id,
            input=input_data,
            name=f"execute_tool [{name}]",
            tags=[INTEGRATION_TAG, "tool", f"tool:{name}"],
        )

    def end_tool(self, run_id: UUID, output: str, status_code: int = 200) -> None:
        """End a tool span."""
        self._handler.end_node(run_id=run_id, output=output, status_code=status_code)
