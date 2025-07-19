from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Metrics")


@_attrs_define
class Metrics:
    """
    Attributes:
        duration_ns (Union[None, Unset, int]): Duration of the trace or span in nanoseconds.  Displayed as 'Latency' in
            Galileo.
    """

    duration_ns: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration_ns: Union[None, Unset, int]
        if isinstance(self.duration_ns, Unset):
            duration_ns = UNSET
        else:
            duration_ns = self.duration_ns

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if duration_ns is not UNSET:
            field_dict["duration_ns"] = duration_ns

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_duration_ns(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        duration_ns = _parse_duration_ns(d.pop("duration_ns", UNSET))

        metrics = cls(duration_ns=duration_ns)

        metrics.additional_properties = d
        return metrics

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
