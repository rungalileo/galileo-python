from enum import Enum


class AgentType(str, Enum):
    CLASSIFIER = "classifier"
    DEFAULT = "default"
    JUDGE = "judge"
    PLANNER = "planner"
    REACT = "react"
    REFLECTION = "reflection"
    ROUTER = "router"
    SUPERVISOR = "supervisor"

    def __str__(self) -> str:
        return str(self.value)
