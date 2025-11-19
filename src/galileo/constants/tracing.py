"""Constants for distributed tracing."""

from galileo.constants import GALILEO_SDK_HEADER_PREFIX

# HTTP header names for propagating distributed tracing context
# These headers follow the pattern of namespaced custom headers (X-Galileo-SDK-*)
TRACE_ID_HEADER = f"{GALILEO_SDK_HEADER_PREFIX}-Trace-ID"
PARENT_ID_HEADER = f"{GALILEO_SDK_HEADER_PREFIX}-Parent-ID"
