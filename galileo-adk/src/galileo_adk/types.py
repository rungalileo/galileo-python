"""Type definitions for Galileo ADK integration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass
class RunContext:
    """Internal context for tracking run state."""

    run_id: UUID
    start_time_ns: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
