"""Constants for distributed tracing."""

from galileo.constants import GALILEO_HEADER_PREFIX

# HTTP header names for propagating distributed tracing context
# These headers follow the pattern of namespaced custom headers (X-Galileo-*)
TRACE_ID_HEADER = f"{GALILEO_HEADER_PREFIX}-Trace-ID"
PARENT_ID_HEADER = f"{GALILEO_HEADER_PREFIX}-Parent-ID"
