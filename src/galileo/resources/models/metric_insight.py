from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.insight_type import InsightType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_insight_categories import MetricInsightCategories
    from ..models.metric_threshold import MetricThreshold


T = TypeVar("T", bound="MetricInsight")


@_attrs_define
class MetricInsight:
    """
    Attributes:
        categories (MetricInsightCategories):
        column_name (str):
        insight_type (InsightType):
        title (str):
        aggregate (Union[None, Unset, float]):
        metric_threshold (Union['MetricThreshold', None, Unset]):
    """

    categories: "MetricInsightCategories"
    column_name: str
    insight_type: InsightType
    title: str
    aggregate: Union[None, Unset, float] = UNSET
    metric_threshold: Union["MetricThreshold", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_threshold import MetricThreshold

        categories = self.categories.to_dict()

        column_name = self.column_name

        insight_type = self.insight_type.value

        title = self.title

        aggregate: Union[None, Unset, float]
        if isinstance(self.aggregate, Unset):
            aggregate = UNSET
        else:
            aggregate = self.aggregate

        metric_threshold: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metric_threshold, Unset):
            metric_threshold = UNSET
        elif isinstance(self.metric_threshold, MetricThreshold):
            metric_threshold = self.metric_threshold.to_dict()
        else:
            metric_threshold = self.metric_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"categories": categories, "column_name": column_name, "insight_type": insight_type, "title": title}
        )
        if aggregate is not UNSET:
            field_dict["aggregate"] = aggregate
        if metric_threshold is not UNSET:
            field_dict["metric_threshold"] = metric_threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric_insight_categories import MetricInsightCategories
        from ..models.metric_threshold import MetricThreshold

        d = src_dict.copy()
        categories = MetricInsightCategories.from_dict(d.pop("categories"))

        column_name = d.pop("column_name")

        insight_type = InsightType(d.pop("insight_type"))

        title = d.pop("title")

        def _parse_aggregate(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        aggregate = _parse_aggregate(d.pop("aggregate", UNSET))

        def _parse_metric_threshold(data: object) -> Union["MetricThreshold", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_threshold_type_0 = MetricThreshold.from_dict(data)

                return metric_threshold_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MetricThreshold", None, Unset], data)

        metric_threshold = _parse_metric_threshold(d.pop("metric_threshold", UNSET))

        metric_insight = cls(
            categories=categories,
            column_name=column_name,
            insight_type=insight_type,
            title=title,
            aggregate=aggregate,
            metric_threshold=metric_threshold,
        )

        metric_insight.additional_properties = d
        return metric_insight

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
