from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
        avg (Union[None, Unset, float]):
        sum_ (Union[None, Unset, float]):
        min_ (Union[None, Unset, float]):
        max_ (Union[None, Unset, float]):
        count (Union[None, Unset, int]):
        pct (Union[None, Unset, float]):
        p50 (Union[None, Unset, float]):
        p90 (Union[None, Unset, float]):
        p95 (Union[None, Unset, float]):
        p99 (Union[None, Unset, float]):
        value_distribution (Union['MetricAggregatesValueDistributionType0', None, Unset]): Distribution of discrete
            values as {value: count}. For boolean metrics: {'0': 2, '1': 8}. For categorical metrics: {'low': 5, 'medium':
            3, 'high': 2}.
    """

    avg: None | Unset | float = UNSET
    sum_: None | Unset | float = UNSET
    min_: None | Unset | float = UNSET
    max_: None | Unset | float = UNSET
    count: None | Unset | int = UNSET
    pct: None | Unset | float = UNSET
    p50: None | Unset | float = UNSET
    p90: None | Unset | float = UNSET
    p95: None | Unset | float = UNSET
    p99: None | Unset | float = UNSET
    value_distribution: Union["MetricAggregatesValueDistributionType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_aggregates_value_distribution_type_0 import MetricAggregatesValueDistributionType0

        avg: None | Unset | float
        avg = UNSET if isinstance(self.avg, Unset) else self.avg

        sum_: None | Unset | float
        sum_ = UNSET if isinstance(self.sum_, Unset) else self.sum_

        min_: None | Unset | float
        min_ = UNSET if isinstance(self.min_, Unset) else self.min_

        max_: None | Unset | float
        max_ = UNSET if isinstance(self.max_, Unset) else self.max_

        count: None | Unset | int
        count = UNSET if isinstance(self.count, Unset) else self.count

        pct: None | Unset | float
        pct = UNSET if isinstance(self.pct, Unset) else self.pct

        p50: None | Unset | float
        p50 = UNSET if isinstance(self.p50, Unset) else self.p50

        p90: None | Unset | float
        p90 = UNSET if isinstance(self.p90, Unset) else self.p90

        p95: None | Unset | float
        p95 = UNSET if isinstance(self.p95, Unset) else self.p95

        p99: None | Unset | float
        p99 = UNSET if isinstance(self.p99, Unset) else self.p99

        value_distribution: None | Unset | dict[str, Any]
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

        def _parse_avg(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        avg = _parse_avg(d.pop("avg", UNSET))

        def _parse_sum_(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        sum_ = _parse_sum_(d.pop("sum", UNSET))

        def _parse_min_(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        min_ = _parse_min_(d.pop("min", UNSET))

        def _parse_max_(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        max_ = _parse_max_(d.pop("max", UNSET))

        def _parse_count(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        count = _parse_count(d.pop("count", UNSET))

        def _parse_pct(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        pct = _parse_pct(d.pop("pct", UNSET))

        def _parse_p50(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        p50 = _parse_p50(d.pop("p50", UNSET))

        def _parse_p90(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        p90 = _parse_p90(d.pop("p90", UNSET))

        def _parse_p95(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        p95 = _parse_p95(d.pop("p95", UNSET))

        def _parse_p99(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        p99 = _parse_p99(d.pop("p99", UNSET))

        def _parse_value_distribution(data: object) -> Union["MetricAggregatesValueDistributionType0", None, Unset]:
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
            return cast(Union["MetricAggregatesValueDistributionType0", None, Unset], data)

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
