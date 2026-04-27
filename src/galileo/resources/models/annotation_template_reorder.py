from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AnnotationTemplateReorder")


@_attrs_define
class AnnotationTemplateReorder:
    """Request to re-order the annotation templates of a project.

    - Expects a list of strings where each string is the ID of a template in the project in the order
    we want the templates to appear in.
    - Expects the list to be complete list of all template IDs.

        Attributes:
            ordering (list[str]):
    """

    ordering: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ordering = self.ordering

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"ordering": ordering})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ordering = cast(list[str], d.pop("ordering"))

        annotation_template_reorder = cls(ordering=ordering)

        annotation_template_reorder.additional_properties = d
        return annotation_template_reorder

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
