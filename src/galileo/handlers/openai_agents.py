import logging
from datetime import datetime
from typing import Any, Optional

from agents import TracingProcessor, tracing

from galileo.decorator import galileo_context
from galileo.logger import GalileoLogger
from galileo.utils.serialization import convert_to_string_dict, serialize_to_str

_logger = logging.getLogger(__name__)


def _get_span_name(span: tracing.Span[Any]) -> str:
    """Get name for a given OpenAI Agent span."""
    if name := getattr(span.span_data, "name", None):
        return str(name)
    elif isinstance(span.span_data, tracing.GenerationSpanData):
        return "Generation"
    elif isinstance(span.span_data, tracing.ResponseSpanData):
        return "Response"
    elif isinstance(span.span_data, tracing.HandoffSpanData):
        return "Handoff"
    elif isinstance(span.span_data, tracing.FunctionSpanData):
        return "FunctionCall"  # More descriptive than 'task' potentially
    elif isinstance(span.span_data, tracing.GuardrailSpanData):
        return "Guardrail"
    elif isinstance(span.span_data, tracing.AgentSpanData):
        return "AgentStep"  # More descriptive than 'task' potentially
    elif isinstance(span.span_data, tracing.CustomSpanData):
        return "CustomStep"
    else:
        # Use the type if available, otherwise fallback
        type_name = span.span_data.type or "UnknownStep"
        return type_name.capitalize()


class GalileoTracingProcessor(TracingProcessor):
    """
    TracingProcessor that logs OpenAI Agent traces and spans to Galileo.

    This processor captures different types of spans from OpenAI Agents and logs them
    using the appropriate Galileo span types (workflow, llm, tool, etc.).
    """

    def __init__(self, galileo_logger: Optional[GalileoLogger] = None, flush_on_chain_end: bool = True) -> None:
        self._galileo_logger: GalileoLogger = galileo_logger or galileo_context.get_logger_instance()
        self._trace_started: set[str] = set()  # Track active traces
        self._flush_on_chain_end: bool = flush_on_chain_end

    def on_trace_start(self, trace: tracing.Trace) -> None:
        """Called when a trace starts. Starts a Galileo trace."""
        try:
            # Use trace name as input, similar to Langchain example's root node
            self._galileo_logger.start_trace(input=trace.name or "Unnamed Agent Trace")
            self._trace_started.add(trace.trace_id)
            _logger.debug(f"Started Galileo trace for agent trace_id: {trace.trace_id}")
        except Exception as e:
            _logger.error(f"Galileo: Error in on_trace_start for trace_id {trace.trace_id}: {e}", exc_info=True)

    def on_trace_end(self, trace: tracing.Trace) -> None:
        """Called when a trace ends. Concludes the Galileo trace."""
        if trace.trace_id not in self._trace_started:
            _logger.warning(f"Galileo: Received on_trace_end for unknown trace_id: {trace.trace_id}")
            return
        try:
            # Conclude the overall trace. Output might be hard to determine here,
            # maybe set a status? The final span's output might be more relevant.
            self._galileo_logger.conclude(output=f"{trace.name}")
            self._trace_started.remove(trace.trace_id)
            _logger.debug(f"Ended Galileo trace for agent trace_id: {trace.trace_id}")
            # Optionally flush here, or rely on shutdown/force_flush
            if self._flush_on_chain_end:
                self._galileo_logger.flush()
        except Exception as e:
            _logger.error(f"Galileo: Error in on_trace_end for trace_id {trace.trace_id}: {e}", exc_info=True)

    def _log_span_start(self, span: tracing.Span[Any]) -> None:
        """Handles the start of any span type by logging to Galileo."""
        name = _get_span_name(span)
        metadata = {"agent_span_id": span.span_id, "agent_trace_id": span.trace_id}
        if parent_id := getattr(span, "parent_id", None):
            metadata["parent_span_id"] = parent_id

        # Default input/output - specific handlers will override
        input_data = None
        tags = None  # Add tags if agent spans support them
        created_at = datetime.fromisoformat(span.started_at) if span.started_at else None

        # --- Map Agent Span Types to Galileo Span Types ---

        if isinstance(span.span_data, tracing.AgentSpanData):
            # Treat Agent steps as workflow spans
            metadata["tools"] = serialize_to_str(span.span_data.tools)
            metadata["handoffs"] = serialize_to_str(span.span_data.handoffs)
            metadata["output_type"] = serialize_to_str(span.span_data.output_type)
            self._galileo_logger.add_workflow_span(
                name=name,
                input="Agent Step Start",  # Input often not known at start
                metadata=convert_to_string_dict(metadata),
                tags=tags,
                created_at=created_at,
            )

        elif isinstance(span.span_data, tracing.ResponseSpanData):
            # Often represents the result of an LLM or tool, log as workflow for now
            # Input might be available here
            input_data = serialize_to_str(span.span_data.input)
            self._galileo_logger.add_workflow_span(  # Or maybe custom?
                name=name, input=input_data, metadata=convert_to_string_dict(metadata), tags=tags, created_at=created_at
            )

        elif isinstance(span.span_data, tracing.FunctionSpanData):
            # Map Function calls to Galileo Tool spans
            input_data = serialize_to_str(span.span_data.input)
            self._galileo_logger.add_tool_span(
                name=name, input=input_data, metadata=convert_to_string_dict(metadata), tags=tags, created_at=created_at
            )

        elif isinstance(span.span_data, tracing.HandoffSpanData):
            # Log Handoffs as workflow steps
            metadata["from_agent"] = serialize_to_str(span.span_data.from_agent)
            metadata["to_agent"] = serialize_to_str(span.span_data.to_agent)
            self._galileo_logger.add_workflow_span(
                name=name,
                input="Handoff Start",
                metadata=convert_to_string_dict(metadata),
                tags=tags,
                created_at=created_at,
            )

        elif isinstance(span.span_data, tracing.GuardrailSpanData):
            # Log Guardrails as workflow steps (or potentially custom?)
            metadata["triggered"] = str(span.span_data.triggered)  # Ensure string
            self._galileo_logger.add_workflow_span(
                name=name,
                input="Guardrail Check",
                metadata=convert_to_string_dict(metadata),
                tags=tags,
                created_at=created_at,
            )

        elif isinstance(span.span_data, tracing.GenerationSpanData):
            # Map Generations to Galileo LLM spans
            input_data = serialize_to_str(span.span_data.input)
            metadata["model_config"] = serialize_to_str(span.span_data.model_config)
            # Extract token usage if available at start (less common)
            prompt_tokens = span.data_usage.usage.get("prompt_tokens") if span.data_usage else None
            self._galileo_logger.add_llm_span(
                name=name,
                input=input_data,
                model=span.span_data.model,
                # temperature might be in model_config, requires parsing
                metadata=convert_to_string_dict(metadata),
                tags=tags,
                num_input_tokens=prompt_tokens,
                # Other LLM params like temperature might need extraction from model_config
                created_at=created_at,
            )

        elif isinstance(span.span_data, tracing.CustomSpanData):
            # Log Custom spans as workflow spans, putting custom data in metadata
            custom_data = span.span_data.data or {}
            input_data = serialize_to_str(custom_data.get("input"))
            # Merge remaining custom data into metadata
            for k, v in custom_data.items():
                if k not in ["input", "output", "metadata", "metrics"]:  # Avoid overwriting standard fields if present
                    metadata[f"custom_{k}"] = serialize_to_str(v)
            if "metadata" in custom_data and isinstance(custom_data["metadata"], dict):
                metadata.update(convert_to_string_dict(custom_data["metadata"]))
            # TODO: Handle custom metrics if Galileo adds explicit support

            self._galileo_logger.add_workflow_span(  # Or add_custom_span if available
                name=name,
                input=input_data or "Custom Step Start",
                metadata=convert_to_string_dict(metadata),
                tags=tags,
                created_at=created_at,
            )
        else:
            # Fallback for unknown span types - log as a generic workflow step
            _logger.warning(f"Galileo: Encountered unknown span data type: {type(span.span_data)}")
            self._galileo_logger.add_workflow_span(
                name=f"Unknown: {name}",
                input="Unknown Step Start",
                metadata=convert_to_string_dict(metadata),
                tags=tags,
                created_at=created_at,
            )

    def on_span_start(self, span: tracing.Span[Any]) -> None:
        """Called when a span starts. Logs the appropriate Galileo span start."""
        if span.trace_id not in self._trace_started:
            _logger.warning(
                f"Galileo: Received on_span_start for unknown trace_id: {span.trace_id}. Span: {span.span_id}"
            )
            # Optionally start a trace here if one isn't active, though ideally it should be.
            # self.on_trace_start(tracing.Trace(trace_id=span.trace_id, name=f"Inferred Trace {span.trace_id}"))
            return  # Or proceed cautiously? Let's return for now to avoid incorrect nesting.

        try:
            self._log_span_start(span)
            _logger.debug(f"Started Galileo span for agent span_id: {span.span_id} (Trace: {span.trace_id})")
        except Exception as e:
            _logger.error(f"Galileo: Error in on_span_start for span_id {span.span_id}: {e}", exc_info=True)

    def _extract_output_and_error(self, span: tracing.Span[Any]) -> tuple[Any, Any]:
        """Extracts primary output and error from different span types."""
        output = None
        error = span.error  # Use span's error attribute first

        if isinstance(span.span_data, tracing.ResponseSpanData):
            if span.span_data.response:
                output = span.span_data.response.output
                # metadata handled at start, usage handled below

        elif isinstance(span.span_data, tracing.FunctionSpanData):
            output = span.span_data.output

        elif isinstance(span.span_data, tracing.GenerationSpanData):
            output = span.span_data.output
            # Tokens handled separately for conclude

        elif isinstance(span.span_data, tracing.CustomSpanData):
            output = span.span_data.data.get("output") if span.span_data.data else None
            # Potential error field in custom data? Galileo expects a single error object.
            if not error and span.span_data.data:
                error = span.span_data.data.get("error")

        # Other types might not have a distinct 'output' field in their span_data
        # We'll rely on the basic structure and potential error on the span itself.
        error_str = serialize_to_str(error)
        if error_str == serialize_to_str(None):
            error_str = None
        return serialize_to_str(output), error_str

    def on_span_end(self, span: tracing.Span[Any]) -> None:
        """Called when a span ends. Concludes the current Galileo span."""
        if span.trace_id not in self._trace_started:
            _logger.warning(
                f"Galileo: Received on_span_end for unknown trace_id: {span.trace_id}. Span: {span.span_id}"
            )
            return

        # Default values in case of early exit or error during processing
        duration_ns = 0
        status_code = 500  # Default to error if we can't process properly
        final_output = "Error during span end processing"

        try:
            output, error = self._extract_output_and_error(span)
            kwargs = {}

            # Calculate duration if timestamps are available
            if span.started_at and span.ended_at:
                # Parse the string date into datetime objects
                started_at = datetime.fromisoformat(span.started_at)
                ended_at = datetime.fromisoformat(span.ended_at)
                duration_ns = int((ended_at - started_at).total_seconds() * 1e9)
            # Determine status code based on the presence of an error in the span data
            status_code = 500 if error else 200

            # Format the final output string
            final_output = f"{output} (Error: {error})" if error else f"{output}"

            # Add LLM-specific metrics on conclude if it's a generation span
            if isinstance(span.span_data, tracing.GenerationSpanData) and span.data_usage:
                usage = span.data_usage.usage or {}
                kwargs["num_output_tokens"] = usage.get("completion_tokens")
                kwargs["total_tokens"] = usage.get("total_tokens")
                # Note: num_input_tokens logged at start if possible

            self._galileo_logger.conclude(
                output=final_output, duration_ns=duration_ns, status_code=status_code, **kwargs
            )
            _logger.debug(f"Ended Galileo span for agent span_id: {span.span_id} (Trace: {span.trace_id})")

        except Exception as e:
            _logger.error(f"Galileo: Error in on_span_end processing for span_id {span.span_id}: {e}", exc_info=True)
            # Attempt to conclude with the error message and default/calculated status/duration
            try:
                # Try to recalculate duration if possible, otherwise use the default 0
                if span.started_at and span.ended_at:
                    # Parse the string date into datetime objects
                    started_at = datetime.fromisoformat(span.started_at)
                    ended_at = datetime.fromisoformat(span.ended_at)
                    duration_ns = int((ended_at - started_at).total_seconds() * 1e9)
                # Ensure status code reflects the processing error
                status_code = 500
                self._galileo_logger.conclude(
                    output=f"Error during span end processing: {e}", duration_ns=duration_ns, status_code=status_code
                )
            except Exception as conclude_e:
                _logger.error(
                    f"Galileo: Failed to conclude span {span.span_id} even after processing error: {conclude_e}",
                    exc_info=True,
                )

    def shutdown(self) -> None:
        """Called when the application stops. Flushes remaining traces."""
        _logger.info("Galileo OpenAI Agents Tracer: Shutdown called, flushing logger.")
        # Conclude any remaining active traces (should ideally be handled by on_trace_end)
        active_traces = list(self._trace_started)
        for trace_id in active_traces:
            _logger.warning(f"Galileo: Forcing conclusion of trace {trace_id} during shutdown.")
            try:
                self._galileo_logger.conclude(output="interrupted")
                self._trace_started.remove(trace_id)
            except Exception as e:
                _logger.error(f"Galileo: Error concluding trace {trace_id} during shutdown: {e}")
        try:
            if self._flush_on_chain_end:
                self._galileo_logger.flush()
        except Exception as e:
            _logger.error(f"Galileo: Error flushing logger during shutdown: {e}", exc_info=True)

    def force_flush(self) -> None:
        """Forces an immediate flush of all queued traces."""
        _logger.info("Galileo OpenAI Agents Tracer: Force flush called.")
        # Conclude any remaining active traces (similar to shutdown)
        active_traces = list(self._trace_started)
        for trace_id in active_traces:
            _logger.warning(f"Galileo: Forcing conclusion of trace {trace_id} during force_flush.")
            try:
                self._galileo_logger.conclude(output="force_flushed")
                self._trace_started.remove(trace_id)
            except Exception as e:
                _logger.error(f"Galileo: Error concluding trace {trace_id} during force_flush: {e}")
        try:
            if self._flush_on_chain_end:
                self._galileo_logger.flush()
        except Exception as e:
            _logger.error(f"Galileo: Error flushing logger during force_flush: {e}", exc_info=True)
