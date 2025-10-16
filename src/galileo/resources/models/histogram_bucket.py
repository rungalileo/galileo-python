from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HistogramBucket")


@_attrs_define
class HistogramBucket:
    """
    Attributes
    ----------
        count (int): Number of data points that fall within this bucket
        lower (float): Lower bound of the histogram bucket (inclusive)
        upper (float): Upper bound of the histogram bucket (exclusive, but inclusive for the last bucket).
    """

    count: int
    lower: float
    upper: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        lower = self.lower

        upper = self.upper

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"count": count, "lower": lower, "upper": upper})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        lower = d.pop("lower")

        upper = d.pop("upper")

        histogram_bucket = cls(count=count, lower=lower, upper=upper)

        histogram_bucket.additional_properties = d
        return histogram_bucket

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
