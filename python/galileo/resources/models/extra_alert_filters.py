from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtraAlertFilters")


@_attrs_define
class ExtraAlertFilters:
    """Extra filters for alerts.

    For simplicity of use, all types should be str to make filtering in the DB easier

        Attributes:
            map_threshold (Union[None, Unset, str]):
    """

    map_threshold: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        map_threshold: Union[None, Unset, str]
        if isinstance(self.map_threshold, Unset):
            map_threshold = UNSET
        else:
            map_threshold = self.map_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_map_threshold(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        map_threshold = _parse_map_threshold(d.pop("map_threshold", UNSET))

        extra_alert_filters = cls(map_threshold=map_threshold)

        extra_alert_filters.additional_properties = d
        return extra_alert_filters

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
