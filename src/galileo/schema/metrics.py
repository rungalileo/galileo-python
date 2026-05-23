import warnings
from collections.abc import Callable, Iterator
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_core.core_schema import ValidationInfo

from galileo_core.schemas.logging.span import Span
from galileo_core.schemas.logging.step import STEP_TYPES_WITH_CHILD_SPANS, StepType
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.metric import MetricValueType
from galileo_core.schemas.shared.scorers.galileo_metrics import GalileoMetrics  # noqa: F401
from galileo_core.schemas.shared.scorers.scorer_name import ScorerName


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
