from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DatasetAppendRowValuesAdditionalPropertyType3")


@_attrs_define
class DatasetAppendRowValuesAdditionalPropertyType3:
    """ """

    additional_properties: dict[str, float | int | None | str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dataset_append_row_values_additional_property_type_3 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> float | int | None | str:
                if data is None:
                    return data
                return cast(float | int | None | str, data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        dataset_append_row_values_additional_property_type_3.additional_properties = additional_properties
        return dataset_append_row_values_additional_property_type_3

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> float | int | None | str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: float | int | None | str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
