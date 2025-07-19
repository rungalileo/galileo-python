from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bucketed_metric_buckets import BucketedMetricBuckets


T = TypeVar("T", bound="BucketedMetric")


@_attrs_define
class BucketedMetric:
    """
    Attributes:
        buckets (BucketedMetricBuckets):
        name (str):
        average (Union[None, Unset, float]):
    """

    buckets: "BucketedMetricBuckets"
    name: str
    average: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        buckets = self.buckets.to_dict()

        name = self.name

        average: Union[None, Unset, float]
        if isinstance(self.average, Unset):
            average = UNSET
        else:
            average = self.average

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"buckets": buckets, "name": name})
        if average is not UNSET:
            field_dict["average"] = average

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bucketed_metric_buckets import BucketedMetricBuckets

        d = dict(src_dict)
        buckets = BucketedMetricBuckets.from_dict(d.pop("buckets"))

        name = d.pop("name")

        def _parse_average(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average = _parse_average(d.pop("average", UNSET))

        bucketed_metric = cls(buckets=buckets, name=name, average=average)

        bucketed_metric.additional_properties = d
        return bucketed_metric

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
