"""Type definitions for Galileo ADK integration."""

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass
class EventData:
    """Streaming event data."""

    event_type: str
    event_id: str | None
    content: str
    is_final: bool = False
    timestamp_ns: int = 0


@dataclass
class RunContext:
    """Internal context for tracking run state."""

    run_id: UUID
    events: list[EventData] = field(default_factory=list)
    start_time_ns: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
