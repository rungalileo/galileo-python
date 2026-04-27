from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.field_type import FieldType
from ..models.operator import Operator
from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryFilterV1")


@_attrs_define
class QueryFilterV1:
    """
    Attributes:
        col_name (str):
        value (Any):
        operator (Operator):
        json_field_type (FieldType | None | Unset):
        value_is_column (bool | None | Unset):  Default: False.
        json_field (None | str | Unset):
        alternate_json_field (None | str | Unset):
    """

    col_name: str
    value: Any
    operator: Operator
    json_field_type: FieldType | None | Unset = UNSET
    value_is_column: bool | None | Unset = False
    json_field: None | str | Unset = UNSET
    alternate_json_field: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        col_name = self.col_name

        value = self.value

        operator = self.operator.value

        json_field_type: None | str | Unset
        if isinstance(self.json_field_type, Unset):
            json_field_type = UNSET
        elif isinstance(self.json_field_type, FieldType):
            json_field_type = self.json_field_type.value
        else:
            json_field_type = self.json_field_type

        value_is_column: bool | None | Unset
        if isinstance(self.value_is_column, Unset):
            value_is_column = UNSET
        else:
            value_is_column = self.value_is_column

        json_field: None | str | Unset
        if isinstance(self.json_field, Unset):
            json_field = UNSET
        else:
            json_field = self.json_field

        alternate_json_field: None | str | Unset
        if isinstance(self.alternate_json_field, Unset):
            alternate_json_field = UNSET
        else:
            alternate_json_field = self.alternate_json_field

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"col_name": col_name, "value": value, "operator": operator})
        if json_field_type is not UNSET:
            field_dict["json_field_type"] = json_field_type
        if value_is_column is not UNSET:
            field_dict["value_is_column"] = value_is_column
        if json_field is not UNSET:
            field_dict["json_field"] = json_field
        if alternate_json_field is not UNSET:
            field_dict["alternate_json_field"] = alternate_json_field

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        col_name = d.pop("col_name")

        value = d.pop("value")

        operator = Operator(d.pop("operator"))

        def _parse_json_field_type(data: object) -> FieldType | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                json_field_type_type_0 = FieldType(data)

                return json_field_type_type_0
            except:  # noqa: E722
                pass
            return cast(FieldType | None | Unset, data)

        json_field_type = _parse_json_field_type(d.pop("json_field_type", UNSET))

        def _parse_value_is_column(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        value_is_column = _parse_value_is_column(d.pop("value_is_column", UNSET))

        def _parse_json_field(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        json_field = _parse_json_field(d.pop("json_field", UNSET))

        def _parse_alternate_json_field(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        alternate_json_field = _parse_alternate_json_field(d.pop("alternate_json_field", UNSET))

        query_filter_v1 = cls(
            col_name=col_name,
            value=value,
            operator=operator,
            json_field_type=json_field_type,
            value_is_column=value_is_column,
            json_field=json_field,
            alternate_json_field=alternate_json_field,
        )

        query_filter_v1.additional_properties = d
        return query_filter_v1

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
