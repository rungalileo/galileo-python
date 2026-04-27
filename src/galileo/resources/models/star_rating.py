from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StarRating")


@_attrs_define
class StarRating:
    """
    Attributes:
        value (int):
        annotation_type (Literal['star'] | Unset):  Default: 'star'.
    """

    value: int
    annotation_type: Literal["star"] | Unset = "star"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        annotation_type = self.annotation_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if annotation_type is not UNSET:
            field_dict["annotation_type"] = annotation_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        annotation_type = cast(Literal["star"] | Unset, d.pop("annotation_type", UNSET))
        if annotation_type != "star" and not isinstance(annotation_type, Unset):
            raise ValueError(f"annotation_type must match const 'star', got '{annotation_type}'")

        star_rating = cls(value=value, annotation_type=annotation_type)

        star_rating.additional_properties = d
        return star_rating

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
