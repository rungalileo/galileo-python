from datetime import datetime
from typing import Dict
from agents import tracing
from galileo.decorator import galileo_context
from galileo_core.schemas.logging.trace import Trace
from galileo.utils import _get_timestamp


class GalileoTracingProcessor(tracing.TracingProcessor):
    """
    `GalileoTracingProcessor` is a `tracing.TracingProcessor` that logs traces to Galileo.
    """

    def __init__(self) -> None:
        self._galileo_logger = galileo_context.get_logger_instance()
        self._spans: Dict[str, Trace] = {}
        self._traces_start_end_times: Dict[str, datetime.datetime] = {}

    def on_trace_start(self, trace: tracing.Trace) -> None:

        self._spans[trace.trace_id] = self._galileo_logger.start_trace(
            # trace_id=trace.trace_id, # TODO FIX,
            name=trace.name,
            type="task",
           
        )
        self._traces_start_end_times[trace.trace_id] = _get_timestamp()
        
    def on_trace_end(self, trace: tracing.Trace) -> None:
        # span = self._spans[trace.trace_id]
        # start_time = self._traces_start_end_times.pop(trace.trace_id)
        # span.duration_ns =  _get_timestamp() - start_time 
        # span.created_at_ns = start_time
        pass
    
    def on_span_start(self, span: tracing.Span[tracing.SpanData]) -> None:
        pass

    def on_span_end(self, span: tracing.Span[tracing.SpanData]) -> None:
    
        stored_span = self._spans[span.trace_id]
        if not stored_span:
            return 
        
        stored_span.add_llm_span(
        input=span.input
    )

    def shutdown(self) -> None:
        self._galileo_logger.flush()

    def force_flush(self) -> None:
        self._galileo_logger.flush()