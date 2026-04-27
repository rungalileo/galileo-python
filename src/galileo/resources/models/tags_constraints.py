from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TagsConstraints")


@_attrs_define
class TagsConstraints:
    """
    Attributes:
        annotation_type (Literal['tags']):
        tags (list[str]):
        allow_other (bool | Unset):  Default: False.
    """

    annotation_type: Literal["tags"]
    tags: list[str]
    allow_other: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        annotation_type = self.annotation_type

        tags = self.tags

        allow_other = self.allow_other

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"annotation_type": annotation_type, "tags": tags})
        if allow_other is not UNSET:
            field_dict["allow_other"] = allow_other

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        annotation_type = cast(Literal["tags"], d.pop("annotation_type"))
        if annotation_type != "tags":
            raise ValueError(f"annotation_type must match const 'tags', got '{annotation_type}'")

        tags = cast(list[str], d.pop("tags"))

        allow_other = d.pop("allow_other", UNSET)

        tags_constraints = cls(annotation_type=annotation_type, tags=tags, allow_other=allow_other)

        tags_constraints.additional_properties = d
        return tags_constraints

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
