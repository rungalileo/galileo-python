from typing import Literal, cast

AgentType = Literal["classifier", "default", "judge", "planner", "react", "reflection", "router", "supervisor"]

AGENT_TYPE_VALUES: set[AgentType] = {
    "classifier",
    "default",
    "judge",
    "planner",
    "react",
    "reflection",
    "router",
    "supervisor",
}


def check_agent_type(value: str) -> AgentType:
    if value in AGENT_TYPE_VALUES:
        return cast(AgentType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AGENT_TYPE_VALUES!r}")
