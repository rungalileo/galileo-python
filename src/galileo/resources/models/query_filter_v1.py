from typing import Any, TypeVar, Union, cast

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
        operator (Operator):
        value (Any):
        alternate_json_field (Union[None, Unset, str]):
        json_field (Union[None, Unset, str]):
        json_field_type (Union[FieldType, None, Unset]):
        value_is_column (Union[None, Unset, bool]):  Default: False.
    """

    col_name: str
    operator: Operator
    value: Any
    alternate_json_field: Union[None, Unset, str] = UNSET
    json_field: Union[None, Unset, str] = UNSET
    json_field_type: Union[FieldType, None, Unset] = UNSET
    value_is_column: Union[None, Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        col_name = self.col_name

        operator = self.operator.value

        value = self.value

        alternate_json_field: Union[None, Unset, str]
        if isinstance(self.alternate_json_field, Unset):
            alternate_json_field = UNSET
        else:
            alternate_json_field = self.alternate_json_field

        json_field: Union[None, Unset, str]
        if isinstance(self.json_field, Unset):
            json_field = UNSET
        else:
            json_field = self.json_field

        json_field_type: Union[None, Unset, str]
        if isinstance(self.json_field_type, Unset):
            json_field_type = UNSET
        elif isinstance(self.json_field_type, FieldType):
            json_field_type = self.json_field_type.value
        else:
            json_field_type = self.json_field_type

        value_is_column: Union[None, Unset, bool]
        if isinstance(self.value_is_column, Unset):
            value_is_column = UNSET
        else:
            value_is_column = self.value_is_column

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"col_name": col_name, "operator": operator, "value": value})
        if alternate_json_field is not UNSET:
            field_dict["alternate_json_field"] = alternate_json_field
        if json_field is not UNSET:
            field_dict["json_field"] = json_field
        if json_field_type is not UNSET:
            field_dict["json_field_type"] = json_field_type
        if value_is_column is not UNSET:
            field_dict["value_is_column"] = value_is_column

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        col_name = d.pop("col_name")

        operator = Operator(d.pop("operator"))

        value = d.pop("value")

        def _parse_alternate_json_field(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        alternate_json_field = _parse_alternate_json_field(d.pop("alternate_json_field", UNSET))

        def _parse_json_field(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        json_field = _parse_json_field(d.pop("json_field", UNSET))

        def _parse_json_field_type(data: object) -> Union[FieldType, None, Unset]:
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
            return cast(Union[FieldType, None, Unset], data)

        json_field_type = _parse_json_field_type(d.pop("json_field_type", UNSET))

        def _parse_value_is_column(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        value_is_column = _parse_value_is_column(d.pop("value_is_column", UNSET))

        query_filter_v1 = cls(
            col_name=col_name,
            operator=operator,
            value=value,
            alternate_json_field=alternate_json_field,
            json_field=json_field,
            json_field_type=json_field_type,
            value_is_column=value_is_column,
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
