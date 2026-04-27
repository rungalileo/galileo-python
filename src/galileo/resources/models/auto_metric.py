from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AutoMetric")


@_attrs_define
class AutoMetric:
    """
    Attributes:
        name (str):
        description (str):
        implementation (str | Unset):  Default: 'galileo'.
        code (str | Unset):  Default: ''.
    """

    name: str
    description: str
    implementation: str | Unset = "galileo"
    code: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        implementation = self.implementation

        code = self.code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "description": description})
        if implementation is not UNSET:
            field_dict["implementation"] = implementation
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        implementation = d.pop("implementation", UNSET)

        code = d.pop("code", UNSET)

        auto_metric = cls(name=name, description=description, implementation=implementation, code=code)

        auto_metric.additional_properties = d
        return auto_metric

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
