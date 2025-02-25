from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.field_type import FieldType
from ..models.sort_direction import SortDirection
from ..types import UNSET, Unset

T = TypeVar("T", bound="SortClause")


@_attrs_define
class SortClause:
    """
    Attributes:
        col_name (str):
        sort_dir (SortDirection):
        json_field (Union[None, Unset, str]):
        json_field_type (Union[FieldType, None, Unset]):
    """

    col_name: str
    sort_dir: SortDirection
    json_field: Union[None, Unset, str] = UNSET
    json_field_type: Union[FieldType, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        col_name = self.col_name

        sort_dir = self.sort_dir.value

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"col_name": col_name, "sort_dir": sort_dir})
        if json_field is not UNSET:
            field_dict["json_field"] = json_field
        if json_field_type is not UNSET:
            field_dict["json_field_type"] = json_field_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        col_name = d.pop("col_name")

        sort_dir = SortDirection(d.pop("sort_dir"))

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

        sort_clause = cls(col_name=col_name, sort_dir=sort_dir, json_field=json_field, json_field_type=json_field_type)

        sort_clause.additional_properties = d
        return sort_clause

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
