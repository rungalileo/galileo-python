"""Span hierarchy management for Galileo ADK."""

from __future__ import annotations

import json
import time
from typing import Any
from uuid import UUID

from galileo.handlers.base_handler import GalileoBaseHandler
from galileo_adk.types import RunContext

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
        self._run_contexts.pop(str(run_id), None)
        self._handler.end_node(run_id=run_id, output=output, status_code=status_code)

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
        metadata: dict[str, Any] | None = None,
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
            metadata=metadata,
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
            output: LLM output - can be a list of Messages or a single value.
                   Normalized before passing to handler:
                   - Empty list -> None
                   - Single-element list -> unwrapped element
                   - Multi-element list -> JSON-serialized string
            num_input_tokens: Number of input tokens used
            num_output_tokens: Number of output tokens generated
            total_tokens: Total tokens used
            status_code: HTTP status code (200 for success)
        """
        if isinstance(output, list):
            if not output:
                normalized_output = None
            elif len(output) == 1:
                normalized_output = output[0]
            else:
                try:
                    serializable = [msg.model_dump() if hasattr(msg, "model_dump") else str(msg) for msg in output]
                    normalized_output = json.dumps(serializable)
                except (TypeError, ValueError):
                    normalized_output = str(output)
        else:
            normalized_output = output

        self._handler.end_node(
            run_id=run_id,
            output=normalized_output,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            total_tokens=total_tokens,
            status_code=status_code,
        )

    def start_tool(
        self,
        run_id: UUID,
        parent_run_id: UUID | None,
        input_data: str,
        name: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Start a tool span."""
        self._handler.start_node(
            node_type="tool",
            parent_run_id=parent_run_id,
            run_id=run_id,
            input=input_data,
            name=f"execute_tool [{name}]",
            tags=[INTEGRATION_TAG, "tool", f"tool:{name}"],
            metadata=metadata,
        )

    def end_tool(self, run_id: UUID, output: str, status_code: int = 200) -> None:
        """End a tool span."""
        self._handler.end_node(run_id=run_id, output=output, status_code=status_code)
