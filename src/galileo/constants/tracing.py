"""Constants for distributed tracing."""

# HTTP header names for propagating distributed tracing context
# These headers follow the pattern of namespaced custom headers (X-Galileo-*)
TRACE_ID_HEADER = "X-Galileo-Trace-ID"
PARENT_ID_HEADER = "X-Galileo-Parent-ID"
