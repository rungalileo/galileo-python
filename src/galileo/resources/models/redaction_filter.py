from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RedactionFilter")


@_attrs_define
class RedactionFilter:
    """A single filter rule for RBAC redaction.

    Attributes:
        user_metadata_key (str):
        user_metadata_values (list[str]):
    """

    user_metadata_key: str
    user_metadata_values: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_metadata_key = self.user_metadata_key

        user_metadata_values = self.user_metadata_values

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"user_metadata_key": user_metadata_key, "user_metadata_values": user_metadata_values})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_metadata_key = d.pop("user_metadata_key")

        user_metadata_values = cast(list[str], d.pop("user_metadata_values"))

        redaction_filter = cls(user_metadata_key=user_metadata_key, user_metadata_values=user_metadata_values)

        redaction_filter.additional_properties = d
        return redaction_filter

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
