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


class _GalileoScorersProxyMeta(type):
    """Metaclass that makes _GalileoScorersProxy behave like an enum type for isinstance/issubclass checks."""

    def __getattribute__(cls, name: str) -> Any:
        # Allow access to special methods and class metadata without warnings
        if name.startswith("_") or name in ("__class__", "__mro__", "__dict__", "__bases__"):
            return type.__getattribute__(cls, name)

        warnings.warn(
            "GalileoScorers is deprecated and will be removed in a future release. Please use GalileoMetrics instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(GalileoMetrics, name)

    def __getitem__(cls, name: str) -> _ScorerName:
        """Support lookup by name like the original Enum (e.g., GalileoScorers['correctness'])."""
        warnings.warn(
            "GalileoScorers is deprecated and will be removed in a future release. Please use GalileoMetrics instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(GalileoMetrics, name)

    def __instancecheck__(cls, instance: Any) -> bool:
        warnings.warn(
            "GalileoScorers is deprecated and will be removed in a future release. Please use GalileoMetrics instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return isinstance(instance, _ScorerName)

    def __subclasscheck__(cls, subclass: type) -> bool:
        warnings.warn(
            "GalileoScorers is deprecated and will be removed in a future release. Please use GalileoMetrics instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return issubclass(subclass, _ScorerName)

    def __iter__(cls) -> Iterator[_ScorerName]:
        warnings.warn(
            "GalileoScorers is deprecated and will be removed in a future release. Please use GalileoMetrics instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return iter(GalileoMetrics)

    def __contains__(cls, item: Any) -> bool:
        warnings.warn(
            "GalileoScorers is deprecated and will be removed in a future release. Please use GalileoMetrics instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        try:
            # allow either enum member or name/value
            if isinstance(item, _ScorerName):
                return item in GalileoMetrics
            if isinstance(item, str):
                return item in (m.name for m in GalileoMetrics) or item in (m.value for m in GalileoMetrics)
            return False
        except Exception:
            return False

    def __dir__(cls) -> list[str]:
        return [m.name for m in GalileoMetrics]

    def __repr__(cls) -> str:  # pragma: no cover - trivial
        return "<deprecated GalileoScorers proxy - use GalileoMetrics>"


class _GalileoScorersProxy(metaclass=_GalileoScorersProxyMeta):
    """Proxy class that forwards to `GalileoMetrics` but emits a deprecation warning on use."""

    def __new__(cls, value: Any) -> _ScorerName:
        """Allow value-based instantiation like the original Enum (e.g., GalileoScorers('correctness'))."""
        warnings.warn(
            "GalileoScorers is deprecated and will be removed in a future release. Please use GalileoMetrics instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return GalileoMetrics(value)


# Backwards-compatible deprecated proxy - now a class instead of an instance
GalileoScorers = _GalileoScorersProxy

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
