import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="BucketedMetrics")


@_attrs_define
class BucketedMetrics:
    """
    Attributes:
        end_bucket_time (datetime.datetime):
        start_bucket_time (datetime.datetime):
    """

    end_bucket_time: datetime.datetime
    start_bucket_time: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        end_bucket_time = self.end_bucket_time.isoformat()

        start_bucket_time = self.start_bucket_time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"end_bucket_time": end_bucket_time, "start_bucket_time": start_bucket_time})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        end_bucket_time = isoparse(d.pop("end_bucket_time"))

        start_bucket_time = isoparse(d.pop("start_bucket_time"))

        bucketed_metrics = cls(end_bucket_time=end_bucket_time, start_bucket_time=start_bucket_time)

        bucketed_metrics.additional_properties = d
        return bucketed_metrics

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
