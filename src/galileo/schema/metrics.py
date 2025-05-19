from typing import Callable, Generic, Optional, TypeVar, Union

from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_core.core_schema import ValidationInfo

from galileo_core.schemas.logging.span import Span
from galileo_core.schemas.logging.step import StepType
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.metric import MetricValueType

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
            if step_type not in [StepType.workflow, StepType.trace]:
                raise ValidationError("aggregatable_types can only contain trace or workflow steps")
        return value
