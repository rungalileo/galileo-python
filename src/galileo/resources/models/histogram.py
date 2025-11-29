from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.histogram_strategy import HistogramStrategy

if TYPE_CHECKING:
    from ..models.histogram_bucket import HistogramBucket


T = TypeVar("T", bound="Histogram")


@_attrs_define
class Histogram:
    """
    Attributes
    ----------
        strategy (HistogramStrategy):
        edges (list[float]): List of bin edges (monotonically increasing, length = number of buckets + 1)
        buckets (list['HistogramBucket']): List of histogram buckets containing the binned data
        total (int): Total number of data points in the histogram.
    """

    strategy: HistogramStrategy
    edges: list[float]
    buckets: list["HistogramBucket"]
    total: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        strategy = self.strategy.value

        edges = self.edges

        buckets = []
        for buckets_item_data in self.buckets:
            buckets_item = buckets_item_data.to_dict()
            buckets.append(buckets_item)

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"strategy": strategy, "edges": edges, "buckets": buckets, "total": total})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.histogram_bucket import HistogramBucket

        d = dict(src_dict)
        strategy = HistogramStrategy(d.pop("strategy"))

        edges = cast(list[float], d.pop("edges"))

        buckets = []
        _buckets = d.pop("buckets")
        for buckets_item_data in _buckets:
            buckets_item = HistogramBucket.from_dict(buckets_item_data)

            buckets.append(buckets_item)

        total = d.pop("total")

        histogram = cls(strategy=strategy, edges=edges, buckets=buckets, total=total)

        histogram.additional_properties = d
        return histogram

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
