"""Constants for distributed tracing."""

from galileo.constants import SPLUNK_AO_HEADER_PREFIX

# HTTP header names for propagating distributed tracing context
# These headers follow the pattern of namespaced custom headers (Splunk-AO-*)
TRACE_ID_HEADER = f"{SPLUNK_AO_HEADER_PREFIX}-Trace-ID"
PARENT_ID_HEADER = f"{SPLUNK_AO_HEADER_PREFIX}-Parent-ID"
