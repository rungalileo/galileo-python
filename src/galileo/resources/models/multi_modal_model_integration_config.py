from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MultiModalModelIntegrationConfig")


@_attrs_define
class MultiModalModelIntegrationConfig:
    """Configuration for multi-modal capabilities (file uploads).

    Attributes:
        max_files (int | None | Unset): Maximum number of files allowed per request. None means no limit.
        max_file_size_bytes (int | None | Unset): Maximum file size in bytes per file. None means no limit.
    """

    max_files: int | None | Unset = UNSET
    max_file_size_bytes: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_files: int | None | Unset
        if isinstance(self.max_files, Unset):
            max_files = UNSET
        else:
            max_files = self.max_files

        max_file_size_bytes: int | None | Unset
        if isinstance(self.max_file_size_bytes, Unset):
            max_file_size_bytes = UNSET
        else:
            max_file_size_bytes = self.max_file_size_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_files is not UNSET:
            field_dict["max_files"] = max_files
        if max_file_size_bytes is not UNSET:
            field_dict["max_file_size_bytes"] = max_file_size_bytes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_max_files(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_files = _parse_max_files(d.pop("max_files", UNSET))

        def _parse_max_file_size_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_file_size_bytes = _parse_max_file_size_bytes(d.pop("max_file_size_bytes", UNSET))

        multi_modal_model_integration_config = cls(max_files=max_files, max_file_size_bytes=max_file_size_bytes)

        multi_modal_model_integration_config.additional_properties = d
        return multi_modal_model_integration_config

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
