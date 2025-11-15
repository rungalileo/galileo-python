from enum import Enum


class InputTypeEnum(str, Enum):
    AGENT_SPANS = "agent_spans"
    BASIC = "basic"
    LLM_SPANS = "llm_spans"
    RETRIEVER_SPANS = "retriever_spans"
    SESSIONS_NORMALIZED = "sessions_normalized"
    SESSIONS_TRACE_IO_ONLY = "sessions_trace_io_only"
    TOOL_SPANS = "tool_spans"
    TRACE_INPUT_ONLY = "trace_input_only"
    TRACE_IO_ONLY = "trace_io_only"
    TRACE_NORMALIZED = "trace_normalized"
    TRACE_OUTPUT_ONLY = "trace_output_only"
    WORKFLOW_SPANS = "workflow_spans"

    def __str__(self) -> str:
        return str(self.value)
