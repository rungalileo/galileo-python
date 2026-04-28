from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_aggregates_value_distribution_type_0 import MetricAggregatesValueDistributionType0


T = TypeVar("T", bound="MetricAggregates")


@_attrs_define
class MetricAggregates:
    """Structured aggregate values for a single metric, computed from ClickHouse row-level data.

    Attributes
    ----------
        avg (float | None | Unset):
        sum_ (float | None | Unset):
        min_ (float | None | Unset):
        max_ (float | None | Unset):
        count (int | None | Unset):
        pct (float | None | Unset):
        p50 (float | None | Unset):
        p90 (float | None | Unset):
        p95 (float | None | Unset):
        p99 (float | None | Unset):
        value_distribution (MetricAggregatesValueDistributionType0 | None | Unset): Distribution of discrete values as
            {value: count}. For boolean metrics: {'0': 2, '1': 8}. For categorical metrics: {'low': 5, 'medium': 3, 'high':
            2}.
    """

    avg: float | None | Unset = UNSET
    sum_: float | None | Unset = UNSET
    min_: float | None | Unset = UNSET
    max_: float | None | Unset = UNSET
    count: int | None | Unset = UNSET
    pct: float | None | Unset = UNSET
    p50: float | None | Unset = UNSET
    p90: float | None | Unset = UNSET
    p95: float | None | Unset = UNSET
    p99: float | None | Unset = UNSET
    value_distribution: MetricAggregatesValueDistributionType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_aggregates_value_distribution_type_0 import MetricAggregatesValueDistributionType0

        avg: float | None | Unset
        avg = UNSET if isinstance(self.avg, Unset) else self.avg

        sum_: float | None | Unset
        sum_ = UNSET if isinstance(self.sum_, Unset) else self.sum_

        min_: float | None | Unset
        min_ = UNSET if isinstance(self.min_, Unset) else self.min_

        max_: float | None | Unset
        max_ = UNSET if isinstance(self.max_, Unset) else self.max_

        count: int | None | Unset
        count = UNSET if isinstance(self.count, Unset) else self.count

        pct: float | None | Unset
        pct = UNSET if isinstance(self.pct, Unset) else self.pct

        p50: float | None | Unset
        p50 = UNSET if isinstance(self.p50, Unset) else self.p50

        p90: float | None | Unset
        p90 = UNSET if isinstance(self.p90, Unset) else self.p90

        p95: float | None | Unset
        p95 = UNSET if isinstance(self.p95, Unset) else self.p95

        p99: float | None | Unset
        p99 = UNSET if isinstance(self.p99, Unset) else self.p99

        value_distribution: dict[str, Any] | None | Unset
        if isinstance(self.value_distribution, Unset):
            value_distribution = UNSET
        elif isinstance(self.value_distribution, MetricAggregatesValueDistributionType0):
            value_distribution = self.value_distribution.to_dict()
        else:
            value_distribution = self.value_distribution

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avg is not UNSET:
            field_dict["avg"] = avg
        if sum_ is not UNSET:
            field_dict["sum"] = sum_
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if count is not UNSET:
            field_dict["count"] = count
        if pct is not UNSET:
            field_dict["pct"] = pct
        if p50 is not UNSET:
            field_dict["p50"] = p50
        if p90 is not UNSET:
            field_dict["p90"] = p90
        if p95 is not UNSET:
            field_dict["p95"] = p95
        if p99 is not UNSET:
            field_dict["p99"] = p99
        if value_distribution is not UNSET:
            field_dict["value_distribution"] = value_distribution

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_aggregates_value_distribution_type_0 import MetricAggregatesValueDistributionType0

        d = dict(src_dict)

        def _parse_avg(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        avg = _parse_avg(d.pop("avg", UNSET))

        def _parse_sum_(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        sum_ = _parse_sum_(d.pop("sum", UNSET))

        def _parse_min_(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        min_ = _parse_min_(d.pop("min", UNSET))

        def _parse_max_(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_ = _parse_max_(d.pop("max", UNSET))

        def _parse_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        count = _parse_count(d.pop("count", UNSET))

        def _parse_pct(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        pct = _parse_pct(d.pop("pct", UNSET))

        def _parse_p50(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        p50 = _parse_p50(d.pop("p50", UNSET))

        def _parse_p90(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        p90 = _parse_p90(d.pop("p90", UNSET))

        def _parse_p95(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        p95 = _parse_p95(d.pop("p95", UNSET))

        def _parse_p99(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        p99 = _parse_p99(d.pop("p99", UNSET))

        def _parse_value_distribution(data: object) -> MetricAggregatesValueDistributionType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MetricAggregatesValueDistributionType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(MetricAggregatesValueDistributionType0 | None | Unset, data)

        value_distribution = _parse_value_distribution(d.pop("value_distribution", UNSET))

        metric_aggregates = cls(
            avg=avg,
            sum_=sum_,
            min_=min_,
            max_=max_,
            count=count,
            pct=pct,
            p50=p50,
            p90=p90,
            p95=p95,
            p99=p99,
            value_distribution=value_distribution,
        )

        metric_aggregates.additional_properties = d
        return metric_aggregates

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
