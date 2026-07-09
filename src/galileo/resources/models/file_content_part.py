from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FileContentPart")


@_attrs_define
class FileContentPart:
    """Reference to a file associated with this message.

    The file_id can be resolved via the ``files`` dict returned on
    trace/span detail responses, which contains metadata such as
    modality, MIME type, and a presigned download URL.

        Attributes:
            file_id (str):
            type_ (Literal['file'] | Unset):  Default: 'file'.
    """

    file_id: str
    type_: Literal["file"] | Unset = "file"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_id = self.file_id

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"file_id": file_id})
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = d.pop("file_id")

        type_ = cast(Literal["file"] | Unset, d.pop("type", UNSET))
        if type_ != "file" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'file', got '{type_}'")

        file_content_part = cls(file_id=file_id, type_=type_)

        file_content_part.additional_properties = d
        return file_content_part

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
