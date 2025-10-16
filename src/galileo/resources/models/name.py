from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Name")


@_attrs_define
class Name:
    """Global name class for handling unique naming across the application.

    Attributes
    ----------
        value (str):
        append_suffix_if_duplicate (Union[Unset, bool]):  Default: False.
    """

    value: str
    append_suffix_if_duplicate: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        append_suffix_if_duplicate = self.append_suffix_if_duplicate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if append_suffix_if_duplicate is not UNSET:
            field_dict["append_suffix_if_duplicate"] = append_suffix_if_duplicate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        append_suffix_if_duplicate = d.pop("append_suffix_if_duplicate", UNSET)

        name = cls(value=value, append_suffix_if_duplicate=append_suffix_if_duplicate)

        name.additional_properties = d
        return name

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
