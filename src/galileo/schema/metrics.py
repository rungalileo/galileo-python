import warnings
from collections.abc import Iterator
from typing import Any, Callable, Generic, Optional, TypeVar, Union

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from galileo_core.schemas.logging.span import Span
from galileo_core.schemas.logging.step import STEP_TYPES_WITH_CHILD_SPANS, StepType
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.metric import MetricValueType
from galileo_core.schemas.shared.scorers.scorer_name import ScorerName as _ScorerName

# Preferred, non-deprecated name for built-in scorer enum
GalileoMetrics = _ScorerName


class _GalileoScorersProxy:
    """Proxy object that forwards to `GalileoMetrics` but emits a deprecation warning on use."""

    def __getattr__(self, name: str) -> Any:
        warnings.warn(
            "GalileoScorers is deprecated and will be removed in a future release. Please use GalileoMetrics instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(GalileoMetrics, name)

    def __iter__(self) -> Iterator[_ScorerName]:
        # Allow iteration over the enum members
        warnings.warn(
            "GalileoScorers is deprecated and will be removed in a future release. Please use GalileoMetrics instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return iter(GalileoMetrics)

    def __dir__(self) -> list[str]:
        return [m.name for m in GalileoMetrics]


# Backwards-compatible deprecated proxy instance
GalileoScorers = _GalileoScorersProxy()

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

    @model_validator(mode="after")
    def validate_name_and_version(self) -> "Metric":
        preset_metric_names = [scorer.value for scorer in GalileoMetrics]
        if self.name in preset_metric_names:
            if self.version is not None:
                raise ValueError(
                    f"Galileo metric's '{self.name}' do not support versioning at this time. Please use the default version."
                )
        return self


# Keep GalileoMetrics as the preferred, non-deprecated name in this module
GalileoMetrics = GalileoMetrics  # alias to the underlying enum
