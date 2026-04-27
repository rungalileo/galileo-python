from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TextConstraints")


@_attrs_define
class TextConstraints:
    """
    Attributes:
        annotation_type (Literal['text']):
    """

    annotation_type: Literal["text"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        annotation_type = self.annotation_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"annotation_type": annotation_type})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        annotation_type = cast(Literal["text"], d.pop("annotation_type"))
        if annotation_type != "text":
            raise ValueError(f"annotation_type must match const 'text', got '{annotation_type}'")

        text_constraints = cls(annotation_type=annotation_type)

        text_constraints.additional_properties = d
        return text_constraints

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
