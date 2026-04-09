import warnings
from collections.abc import Callable, Iterator
from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_core.core_schema import ValidationInfo

from galileo_core.schemas.logging.span import Span
from galileo_core.schemas.logging.step import STEP_TYPES_WITH_CHILD_SPANS, StepType
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.metric import MetricValueType
from galileo_core.schemas.shared.scorers.scorer_name import ScorerName


class GalileoMetrics(str, Enum):
    """Built-in Galileo metric scorers.

    Values are human-readable UI labels used for scorer lookup via the API.
    Member names follow the convention: base name = LLM version, _luna suffix = SLM version.
    """

    action_advancement = "Action Advancement"
    action_advancement_luna = "Action Advancement (SLM)"
    action_completion = "Action Completion"
    action_completion_luna = "Action Completion (SLM)"
    agent_efficiency = "Agent Efficiency"
    agent_flow = "Agent Flow"
    chunk_attribution_utilization = "Chunk Attribution Utilization"
    chunk_attribution_utilization_luna = "Chunk Attribution Utilization (SLM)"
    chunk_relevance = "Chunk Relevance"
    completeness = "Completeness"
    completeness_luna = "Completeness (SLM)"
    context_adherence = "Context Adherence"
    context_adherence_luna = "Context Adherence (SLM)"
    context_precision = "Context Precision"
    context_relevance = "Context Relevance"
    context_relevance_luna = "Context Relevance (SLM)"
    conversation_quality = "Conversation Quality"
    correctness = "Correctness"
    ground_truth_adherence = "Ground Truth Adherence"
    input_pii = "Input PII"
    input_pii_luna = "Input PII (SLM)"
    input_sexism = "Input Sexism"
    input_sexism_luna = "Input Sexism (SLM)"
    input_tone = "Input Tone"
    input_tone_luna = "Input Tone (SLM)"
    input_toxicity = "Input Toxicity"
    input_toxicity_luna = "Input Toxicity (SLM)"
    instruction_adherence = "Instruction Adherence"
    output_pii = "Output PII"
    output_pii_luna = "Output PII (SLM)"
    output_sexism = "Output Sexism"
    output_sexism_luna = "Output Sexism (SLM)"
    output_tone = "Output Tone"
    output_tone_luna = "Output Tone (SLM)"
    output_toxicity = "Output Toxicity"
    output_toxicity_luna = "Output Toxicity (SLM)"
    precision_at_k = "Precision@K"
    prompt_injection = "Prompt Injection"
    prompt_injection_luna = "Prompt Injection (SLM)"
    reasoning_coherence = "Reasoning Coherence"
    sql_adherence = "SQL Adherence"
    sql_correctness = "SQL Correctness"
    sql_efficiency = "SQL Efficiency"
    sql_injection = "SQL Injection"
    tool_error_rate = "Tool Error Rate"
    tool_error_rate_luna = "Tool Error Rate (SLM)"
    tool_selection_quality = "Tool Selection Quality"
    tool_selection_quality_luna = "Tool Selection Quality (SLM)"
    user_intent_change = "User Intent Change"


class _GalileoScorersProxyMeta(type):
    """Metaclass that makes GalileoScorers a deprecated proxy for ScorerName."""

    _DEPRECATION_MSG = (
        "GalileoScorers is deprecated and will be removed in a future release. Use galileo_core ScorerName instead."
    )

    def __getattribute__(cls, name: str) -> Any:
        if name.startswith("_") or name in ("__class__", "__mro__", "__dict__", "__bases__"):
            return type.__getattribute__(cls, name)
        warnings.warn(cls._DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        return getattr(ScorerName, name)

    def __getitem__(cls, name: str) -> ScorerName:
        warnings.warn(cls._DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        return ScorerName[name]

    def __instancecheck__(cls, instance: Any) -> bool:
        return isinstance(instance, ScorerName)

    def __subclasscheck__(cls, subclass: type) -> bool:
        return issubclass(subclass, ScorerName)

    def __iter__(cls) -> Iterator[ScorerName]:
        warnings.warn(cls._DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        return iter(ScorerName)

    def __contains__(cls, item: Any) -> bool:
        warnings.warn(cls._DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        return item in ScorerName

    def __dir__(cls) -> list[str]:
        return [m.name for m in ScorerName]

    def __repr__(cls) -> str:
        return "<deprecated GalileoScorers proxy - use ScorerName>"


class _GalileoScorersProxy(metaclass=_GalileoScorersProxyMeta):
    """Deprecated proxy that forwards to ScorerName."""

    def __new__(cls, value: Any) -> ScorerName:
        warnings.warn(_GalileoScorersProxyMeta._DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        return ScorerName(value)


GalileoScorers = _GalileoScorersProxy


MetricType = TypeVar("MetricType", bound=MetricValueType)


class LocalMetricConfig(BaseModel, Generic[MetricType]):
    name: str = Field(description="Name of the local metric")
    scorer_fn: Callable[[Trace | Span], MetricType] = Field(
        description="function to call to produce the metric value (takes a trace or span as input"
    )
    aggregator_fn: Callable[[list[MetricType]], MetricType | dict[str, MetricType]] | None = Field(
        default=None,
        description="function to call to produce the aggregate metric values from individual metric values",
    )
    scorable_types: list[StepType] = Field(default=[StepType.llm])
    aggregatable_types: list[StepType] = Field(default=[StepType.trace])

    @field_validator("aggregatable_types", mode="before")
    def set_aggregatable_types(cls, value: list[StepType], info: ValidationInfo) -> list[StepType]:
        if "scorable_types" in info.data and any(
            scorable_type in value for scorable_type in info.data["scorable_types"]
        ):
            raise ValidationError("aggregatable_types cannot contain any types in scorable_types")
        for step_type in value:
            if step_type not in STEP_TYPES_WITH_CHILD_SPANS:
                raise ValidationError("aggregatable_types can only contain trace or workflow steps")
        return value


class Metric(BaseModel):
    name: str = Field(
        description="The name of the metric you want to run a specific version of (ie: 'Sentence Density')."
    )
    version: int | None = Field(
        default=None,
        description="The version of the metric (ie: 1, 2, 3, etc.). If None is provided, the 'default' version will be used.",
    )
