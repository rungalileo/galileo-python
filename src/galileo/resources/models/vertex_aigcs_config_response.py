from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VertexAIGCSConfigResponse")


@_attrs_define
class VertexAIGCSConfigResponse:
    """GCS config response model — credentials are never exposed in GET responses.

    Attributes
    ----------
        bucket_name (str):
        object_path_prefix (str):
    """

    bucket_name: str
    object_path_prefix: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bucket_name = self.bucket_name

        object_path_prefix = self.object_path_prefix

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"bucket_name": bucket_name, "object_path_prefix": object_path_prefix})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bucket_name = d.pop("bucket_name")

        object_path_prefix = d.pop("object_path_prefix")

        vertex_aigcs_config_response = cls(bucket_name=bucket_name, object_path_prefix=object_path_prefix)

        vertex_aigcs_config_response.additional_properties = d
        return vertex_aigcs_config_response

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
