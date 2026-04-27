from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AnnotationTemplateUpdate")


@_attrs_define
class AnnotationTemplateUpdate:
    """
    Attributes:
        name (str):
        criteria (None | str):
    """

    name: str
    criteria: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        criteria: None | str
        criteria = self.criteria

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "criteria": criteria})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_criteria(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        criteria = _parse_criteria(d.pop("criteria"))

        annotation_template_update = cls(name=name, criteria=criteria)

        annotation_template_update.additional_properties = d
        return annotation_template_update

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
