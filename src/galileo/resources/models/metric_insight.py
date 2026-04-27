from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

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
        title (str):
        column_name (str):
        insight_type (InsightType):
        categories (MetricInsightCategories):
        aggregate (float | None | Unset):
        metric_threshold (MetricThreshold | None | Unset):
    """

    title: str
    column_name: str
    insight_type: InsightType
    categories: MetricInsightCategories
    aggregate: float | None | Unset = UNSET
    metric_threshold: MetricThreshold | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_threshold import MetricThreshold

        title = self.title

        column_name = self.column_name

        insight_type = self.insight_type.value

        categories = self.categories.to_dict()

        aggregate: float | None | Unset
        if isinstance(self.aggregate, Unset):
            aggregate = UNSET
        else:
            aggregate = self.aggregate

        metric_threshold: dict[str, Any] | None | Unset
        if isinstance(self.metric_threshold, Unset):
            metric_threshold = UNSET
        elif isinstance(self.metric_threshold, MetricThreshold):
            metric_threshold = self.metric_threshold.to_dict()
        else:
            metric_threshold = self.metric_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"title": title, "column_name": column_name, "insight_type": insight_type, "categories": categories}
        )
        if aggregate is not UNSET:
            field_dict["aggregate"] = aggregate
        if metric_threshold is not UNSET:
            field_dict["metric_threshold"] = metric_threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_insight_categories import MetricInsightCategories
        from ..models.metric_threshold import MetricThreshold

        d = dict(src_dict)
        title = d.pop("title")

        column_name = d.pop("column_name")

        insight_type = InsightType(d.pop("insight_type"))

        categories = MetricInsightCategories.from_dict(d.pop("categories"))

        def _parse_aggregate(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        aggregate = _parse_aggregate(d.pop("aggregate", UNSET))

        def _parse_metric_threshold(data: object) -> MetricThreshold | None | Unset:
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
            return cast(MetricThreshold | None | Unset, data)

        metric_threshold = _parse_metric_threshold(d.pop("metric_threshold", UNSET))

        metric_insight = cls(
            title=title,
            column_name=column_name,
            insight_type=insight_type,
            categories=categories,
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
