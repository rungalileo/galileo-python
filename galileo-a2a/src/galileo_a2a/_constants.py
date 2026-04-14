"""Constants for galileo-a2a instrumentation."""

# Instrumentor identity
from galileo_a2a._version import __version__

INSTRUMENTOR_NAME = "galileo-a2a"
INSTRUMENTOR_VERSION = __version__

# Metadata keys for in-band trace context propagation
GALILEO_OBSERVE_KEY = "galileo_observe"
AGNTCY_OBSERVE_KEY = "observe"  # compatibility with AGNTCY Observe SDK

# A2A span attribute keys (match API-side A2A extension expectations)
A2A_TASK_ID = "a2a.task.id"
A2A_CONTEXT_ID = "a2a.context_id"
A2A_RPC_METHOD = "a2a.rpc.method"
A2A_TASK_STATE = "a2a.task.state"

# OTel GenAI semantic convention attributes — span type determination
GENAI_OPERATION_NAME = "gen_ai.operation.name"
GENAI_AGENT_NAME = "gen_ai.agent.name"
GENAI_SYSTEM = "gen_ai.system"
GENAI_TOOL_NAME = "gen_ai.tool.name"

# OTel GenAI semantic convention attributes — input/output content
GENAI_INPUT_MESSAGES = "gen_ai.input.messages"
GENAI_OUTPUT_MESSAGES = "gen_ai.output.messages"

# OTel GenAI semantic convention attributes — finish reason
GENAI_RESPONSE_FINISH_REASONS = "gen_ai.response.finish_reasons"

# Message roles
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"

# Finish reasons
FINISH_REASON_STOP = "stop"

# Session correlation
SESSION_ID = "session.id"

# Span link attributes for cross-agent correlation
LINK_TYPE = "link.type"
LINK_TYPE_AGENT_HANDOFF = "agent_handoff"
LINK_FROM_AGENT = "link.from_agent"

# A2A task states that indicate errors
ERROR_STATES = frozenset({"failed", "rejected", "canceled"})
