from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.operator import Operator

T = TypeVar("T", bound="ValuePromptFilterParam")


@_attrs_define
class ValuePromptFilterParam:
    """
    Attributes:
        column (str):
        filter_type (Literal['value']):
        value (bool | float | int | str):
        relation (Operator):
    """

    column: str
    filter_type: Literal["value"]
    value: bool | float | int | str
    relation: Operator
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column = self.column

        filter_type = self.filter_type

        value: bool | float | int | str
        value = self.value

        relation = self.relation.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"column": column, "filter_type": filter_type, "value": value, "relation": relation})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        column = d.pop("column")

        filter_type = cast(Literal["value"], d.pop("filter_type"))
        if filter_type != "value":
            raise ValueError(f"filter_type must match const 'value', got '{filter_type}'")

        def _parse_value(data: object) -> bool | float | int | str:
            return cast(bool | float | int | str, data)

        value = _parse_value(d.pop("value"))

        relation = Operator(d.pop("relation"))

        value_prompt_filter_param = cls(column=column, filter_type=filter_type, value=value, relation=relation)

        value_prompt_filter_param.additional_properties = d
        return value_prompt_filter_param

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
