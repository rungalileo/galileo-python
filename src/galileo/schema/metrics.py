from enum import Enum
from typing import Callable, Generic, Optional, TypeVar, Union

from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_core.core_schema import ValidationInfo

from galileo_core.schemas.logging.span import Span
from galileo_core.schemas.logging.step import STEP_TYPES_WITH_CHILD_SPANS, StepType
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.metric import MetricValueType


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


MetricType = TypeVar("MetricType", bound=MetricValueType)


class LocalMetricConfig(BaseModel, Generic[MetricType]):
    name: str = Field(description="Name of the local metric")
    scorer_fn: Callable[[Union[Trace, Span]], MetricType] = Field(
        description="function to call to produce the metric value (takes a trace or span as input"
    )
    aggregator_fn: Optional[Callable[[list[MetricType]], Union[MetricType, dict[str, MetricType]]]] = Field(
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
    version: Optional[int] = Field(
        default=None,
        description="The version of the metric (ie: 1, 2, 3, etc.). If None is provided, the 'default' version will be used.",
    )
