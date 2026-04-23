from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, PrivateAttr

from galileo_core.schemas.logging.step import Metrics

try:
    from galileo_core.schemas.logging.control import ControlAppliesTo, ControlCheckStage, ControlResult
    from galileo_core.schemas.logging.span import ControlSpan

    HAS_NATIVE_CONTROL_SPAN = True
except ImportError:
    HAS_NATIVE_CONTROL_SPAN = False

    class ControlAppliesTo(str, Enum):
        llm_call = "llm_call"
        tool_call = "tool_call"

    class ControlCheckStage(str, Enum):
        pre = "pre"
        post = "post"

    class ControlAction(str, Enum):
        deny = "deny"
        steer = "steer"
        observe = "observe"

    class ControlResult(BaseModel):
        action: ControlAction = Field(description="Decision/action produced by the control.")
        matched: bool = Field(
            description=(
                "Whether the control matched. False covers both non-match and error cases; "
                "use error_message to distinguish errors."
            )
        )
        confidence: float | None = Field(
            default=None,
            description="Confidence score reported by the control evaluation result.",
        )
        error_message: str | None = Field(
            default=None,
            description="Error text when control evaluation failed.",
        )

    class ControlSpan(BaseModel):
        """Fallback ControlSpan compatible with the Orbit schema."""

        type: Literal["control"] = Field(default="control", description="Type of the span.")
        input: Any = Field(default="", description="Representative input selected for the control evaluation.")
        redacted_input: Any | None = Field(default=None, description="Redacted representative control input.")
        output: ControlResult | None = Field(default=None, description="Structured control evaluation result.")
        redacted_output: ControlResult | None = Field(
            default=None,
            description="Redacted structured control evaluation result.",
        )
        name: str = Field(default="control", description="Human-readable control name.")
        created_at: datetime = Field(
            default_factory=lambda: datetime.now(tz=timezone.utc),
            description="Timestamp of the control execution.",
        )
        user_metadata: dict[str, str] = Field(default_factory=dict, description="Metadata associated with the span.")
        tags: list[str] = Field(default_factory=list, description="Tags associated with the span.")
        status_code: int | None = Field(default=None, description="Status code associated with the span.")
        metrics: Metrics = Field(default_factory=Metrics, description="Metrics associated with the span.")
        external_id: str | None = Field(default=None, description="User-provided external identifier.")
        dataset_input: str | None = Field(default=None, description="Dataset input inherited from the parent.")
        dataset_output: str | None = Field(default=None, description="Dataset output inherited from the parent.")
        dataset_metadata: dict[str, str] = Field(
            default_factory=dict,
            description="Dataset metadata inherited from the parent.",
        )
        id: Any | None = Field(default=None, description="Galileo ID of the control span.")
        session_id: Any | None = Field(default=None, description="Session ID associated with the span.")
        trace_id: Any | None = Field(default=None, description="Trace ID associated with the span.")
        parent_id: Any | None = Field(default=None, description="Parent span ID associated with the span.")
        step_number: int | None = Field(default=None, description="Topological step number of the span.")
        control_id: int | None = Field(default=None, description="Identifier of the control definition.")
        agent_name: str | None = Field(default=None, description="Agent name associated with the control execution.")
        check_stage: ControlCheckStage | None = Field(default=None, description="Control execution stage.")
        applies_to: ControlAppliesTo | None = Field(default=None, description="Parent execution type.")
        evaluator_name: str | None = Field(default=None, description="Representative evaluator name.")
        selector_path: str | None = Field(default=None, description="Representative selector path.")
        _parent: Any = PrivateAttr(default=None)
