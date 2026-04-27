from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OrgMetadataDeleteRequest")


@_attrs_define
class OrgMetadataDeleteRequest:
    """Request body for organization-wide metadata-based deletion.

    Attributes:
        metadata_key (str):
        metadata_value (str):
    """

    metadata_key: str
    metadata_value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata_key = self.metadata_key

        metadata_value = self.metadata_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"metadata_key": metadata_key, "metadata_value": metadata_value})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metadata_key = d.pop("metadata_key")

        metadata_value = d.pop("metadata_value")

        org_metadata_delete_request = cls(metadata_key=metadata_key, metadata_value=metadata_value)

        org_metadata_delete_request.additional_properties = d
        return org_metadata_delete_request

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
