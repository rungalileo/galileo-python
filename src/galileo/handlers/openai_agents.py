import logging
from datetime import datetime, timezone
from typing import Any

from agents import Span, Trace, TracingProcessor

from galileo import galileo_context
from galileo.logger import GalileoLogger
from galileo.schema.handler import Node
from galileo.utils import _get_timestamp
from galileo.utils.openai_agents import (
    _extract_llm_data,
    _extract_tool_data,
    _extract_workflow_data,
    _get_galileo_span_type,
    _get_span_name,
)
from galileo.utils.serialization import convert_to_string_dict, serialize_to_str

_logger = logging.getLogger(__name__)


class GalileoTracingProcessor(TracingProcessor):
    """
    OpenAI Agents TracingProcessor implementation for logging traces to Galileo.

    Builds a tree of spans during agent execution and logs them hierarchically
    to Galileo upon trace completion.

    Attributes
    ----------
    _galileo_logger : GalileoLogger
        The Galileo logger instance.
    _start_new_trace : bool
        Whether to start a new Galileo trace for each OpenAI Agent trace.
    _flush_on_trace_end : bool
        Whether to automatically flush the log batch to Galileo when a trace ends.
    _nodes : dict[str, Node]
        Stores Node objects keyed by their OpenAI span_id or trace_id (for root).
    """

    def __init__(
        self, galileo_logger: GalileoLogger | None = None, start_new_trace: bool = True, flush_on_trace_end: bool = True
    ):
        self._galileo_logger: GalileoLogger = galileo_logger or galileo_context.get_logger_instance()
        self._start_new_trace: bool = start_new_trace
        self._flush_on_trace_end: bool = flush_on_trace_end
        self._nodes: dict[str, Node] = {}
        self._root_node: str | None = None

    def on_trace_start(self, trace: Trace) -> None:
        """Called when an OpenAI Agent trace starts."""

        node = Node(
            node_type="agent",
            run_id=trace.trace_id,
            span_params={
                "start_time": _get_timestamp(),
                "name": trace.name,
                "metadata": convert_to_string_dict(trace.metadata),
            },
        )

        self._nodes[trace.trace_id] = node
        self._root_node = trace.trace_id

    def on_trace_end(self, trace: Trace) -> None:
        """Called when an OpenAI Agent trace ends."""
        node = self._nodes.get(trace.trace_id)
        if not node:
            _logger.warning(f"End called for unknown trace_id {trace.trace_id}")
            return

        node.span_params["duration_ns"] = (_get_timestamp() - node.span_params["start_time"]).total_seconds() * 1e9
        # Log the trace to Galileo
        if node.run_id == self._root_node:
            self._commit_trace()

        # Optionally flush the log batch
        if self._flush_on_trace_end:
            self._galileo_logger.flush()

    def _commit_trace(self) -> None:
        if not self._nodes:
            _logger.warning("No nodes to commit")
            return
        root_node = self._nodes[self._root_node]
        if root_node is None:
            _logger.warning("Unable to add nodes to trace: Root node not set")
            return
        self._galileo_logger.start_trace(
            input=root_node.span_params.get("name", ""),
            name=root_node.span_params.get("name", ""),
            duration_ns=root_node.span_params.get("duration_ns"),
            created_at=root_node.span_params.get("start_time"),
            metadata=root_node.span_params.get("metadata", {}),
        )

        self._log_node_tree(root_node)

        self._galileo_logger.conclude(output=root_node.span_params.get("name", ""))

    def _log_node_tree(self, node: Node) -> None:
        """
        Log a node and its children recursively.

        Parameters
        ----------
        node : Node
            The node to log.
        """
        is_workflow_span = False
        input = node.span_params.get("input", "")
        output = node.span_params.get("output", "")
        name = node.span_params.get("name")
        metadata = node.span_params.get("metadata")
        tags = node.span_params.get("tags")

        # Convert metadata to a dict[str, str]
        if metadata is not None:
            metadata = convert_to_string_dict(metadata)

        # Log the current node based on its type
        if node.node_type in ("agent", "chain", "workflow"):
            self._galileo_logger.add_workflow_span(
                input=input,
                output=output,
                name=name,
                metadata=metadata,
                tags=tags,
                duration_ns=node.span_params.get("duration_ns"),
            )
            is_workflow_span = True
        elif node.node_type in ("llm", "chat"):
            self._galileo_logger.add_llm_span(
                input=input,
                output=output,
                model=node.span_params.get("model"),
                temperature=node.span_params.get("temperature"),
                name=name,
                metadata=metadata,
                tags=tags,
                num_input_tokens=node.span_params.get("num_input_tokens"),
                num_output_tokens=node.span_params.get("num_output_tokens"),
                total_tokens=node.span_params.get("total_tokens"),
                time_to_first_token_ns=node.span_params.get("time_to_first_token_ns"),
                duration_ns=node.span_params.get("duration_ns"),
            )
        elif node.node_type == "retriever":
            self._galileo_logger.add_retriever_span(
                input=input,
                output=output,
                name=name,
                metadata=metadata,
                tags=tags,
                duration_ns=node.span_params.get("duration_ns"),
            )
        elif node.node_type == "tool":
            self._galileo_logger.add_tool_span(
                input=input,
                output=output,
                name=name,
                metadata=metadata,
                tags=tags,
                duration_ns=node.span_params.get("duration_ns"),
            )
        else:
            _logger.warning(f"Unknown node type: {node.node_type}")

        # Process all child nodes
        last_child = None
        for child_id in node.children:
            child_node = self._nodes.get(child_id)
            if child_node:
                self._log_node_tree(child_node)
                last_child = child_node
            else:
                _logger.warning(f"Child node {child_id} not found")

        # Conclude workflow span. Use the last child's output if necessary
        if is_workflow_span:
            output = output or (last_child.span_params.get("output", "") if last_child else "")
            self._galileo_logger.conclude(output=serialize_to_str(output))

    def on_span_start(self, span: Span[Any]) -> None:
        """Called when an OpenAI Agent span starts."""

        span_id = span.span_id
        trace_id = span.trace_id
        parent_id = span.parent_id or trace_id  # Parent is previous span or root trace

        if span_id in self._nodes:
            _logger.warning(f"Span node already exists for span_id {span_id}, overwriting...")

        # Determine span type and name
        galileo_type = _get_galileo_span_type(span.span_data)
        span_name = _get_span_name(span)

        # Extract initial data based on type
        initial_params: dict[str, Any] = {
            "name": span_name,
            "start_time_iso": span.started_at or datetime.now(timezone.utc).isoformat(),
        }
        if galileo_type == "llm":
            llm_data = _extract_llm_data(span.span_data)
            initial_params.update(
                {
                    "input": llm_data.get("input"),
                    "model": llm_data.get("model"),
                    "temperature": llm_data.get("temperature"),
                    "tools": llm_data.get("tools"),
                    "model_parameters": llm_data.get("model_parameters"),
                    "metadata": llm_data.get("metadata", {}),
                    "status_code": llm_data.get("status_code", 200),
                }
            )
        elif galileo_type == "tool":
            tool_data = _extract_tool_data(span.span_data)
            initial_params.update(
                {
                    "input": tool_data.get("input"),
                    "metadata": tool_data.get("metadata", {}),
                    "status_code": tool_data.get("status_code", 200),
                }
            )
        elif galileo_type == "workflow":
            wf_data = _extract_workflow_data(span.span_data)
            initial_params.update(
                {
                    "input": wf_data.get("input"),
                    "metadata": wf_data.get("metadata", {}),
                    "status_code": wf_data.get("status_code", 200),
                }
            )

        # Create the node
        node = Node(node_type=galileo_type, span_params=initial_params, run_id=span_id, parent_run_id=parent_id)
        self._nodes[span_id] = node

        # Add to parent's children list
        parent_node = self._nodes.get(parent_id)
        if parent_node:
            parent_node.children.append(span_id)
        else:
            _logger.warning(f"Parent node {parent_id} not found for span {span_id} in trace {trace_id}")

    def on_span_end(self, span: Span[Any]) -> None:
        """Called when an OpenAI Agent span ends."""

        span_id = span.span_id
        node = self._nodes.get(span_id)

        if not node:
            _logger.warning(f"End called for unknown span_id {span_id}")
            return

        # Update node with final data
        galileo_type = node.node_type
        end_params: dict[str, Any] = {"end_time_iso": span.ended_at or datetime.now(timezone.utc).isoformat()}
        end_params["duration_ns"] = (
            datetime.fromisoformat(span.ended_at) - datetime.fromisoformat(node.span_params["start_time_iso"])
        ).total_seconds() * 1e9

        if galileo_type == "llm":
            llm_data = _extract_llm_data(span.span_data)
            end_params.update(
                {
                    "output": llm_data.get("output"),
                    "num_input_tokens": llm_data.get("num_input_tokens"),
                    "num_output_tokens": llm_data.get("num_output_tokens"),
                    "total_tokens": llm_data.get("total_tokens"),
                    # Overwrite metadata if new info available
                    "metadata": {**node.span_params.get("metadata", {}), **llm_data.get("metadata", {})},
                    "status_code": llm_data.get("status_code", node.span_params.get("status_code", 200)),
                }
            )
            # Ensure input is preserved if it wasn't available at start
            if node.span_params.get("input") is None:
                node.span_params["input"] = llm_data.get("input")

        elif galileo_type == "tool":
            tool_data = _extract_tool_data(span.span_data)
            end_params.update(
                {
                    "output": tool_data.get("output"),
                    "metadata": {**node.span_params.get("metadata", {}), **tool_data.get("metadata", {})},
                    "status_code": tool_data.get("status_code", node.span_params.get("status_code", 200)),
                }
            )
            if node.span_params.get("input") is None:
                node.span_params["input"] = tool_data.get("input")

        elif galileo_type == "workflow":
            wf_data = _extract_workflow_data(span.span_data)
            end_params.update(
                {
                    "output": wf_data.get("output"),
                    "metadata": {**node.span_params.get("metadata", {}), **wf_data.get("metadata", {})},
                    "status_code": wf_data.get("status_code", node.span_params.get("status_code", 200)),
                }
            )
            # Workflow output might only be known at the end
            if node.span_params.get("output") is None:
                node.span_params["output"] = wf_data.get("output")

        # Handle errors
        if error := span.error:
            end_params["error"] = error  # Store raw error
            end_params["status_code"] = 500  # Indicate error status
            end_params["metadata"] = {
                **end_params.get("metadata", {}),
                "error_message": error.get("message", str(error)),
                "error_type": error.get("type", type(error).__name__),
                "error_details": serialize_to_str(error.get("data")),
            }

        # Update the node's parameters
        node.span_params.update(end_params)

    def shutdown(self) -> None:
        """Called when the application stops. Flushes any remaining logs."""

        self._galileo_logger.flush()

    def force_flush(self) -> None:
        """Forces an immediate flush of all queued traces/spans."""
        self._galileo_logger.flush()
