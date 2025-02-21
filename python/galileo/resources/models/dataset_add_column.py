from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetAddColumn")


@_attrs_define
class DatasetAddColumn:
    """
    Attributes:
        column_values (list[Union[None, float, int, str]]):
        new_column_name (str):
        edit_type (Union[Literal['add_column'], Unset]):  Default: 'add_column'.
    """

    column_values: list[Union[None, float, int, str]]
    new_column_name: str
    edit_type: Union[Literal["add_column"], Unset] = "add_column"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_values = []
        for column_values_item_data in self.column_values:
            column_values_item: Union[None, float, int, str]
            column_values_item = column_values_item_data
            column_values.append(column_values_item)

        new_column_name = self.new_column_name

        edit_type = self.edit_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"column_values": column_values, "new_column_name": new_column_name})
        if edit_type is not UNSET:
            field_dict["edit_type"] = edit_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        column_values = []
        _column_values = d.pop("column_values")
        for column_values_item_data in _column_values:

            def _parse_column_values_item(data: object) -> Union[None, float, int, str]:
                if data is None:
                    return data
                return cast(Union[None, float, int, str], data)

            column_values_item = _parse_column_values_item(column_values_item_data)

            column_values.append(column_values_item)

        new_column_name = d.pop("new_column_name")

        edit_type = cast(Union[Literal["add_column"], Unset], d.pop("edit_type", UNSET))
        if edit_type != "add_column" and not isinstance(edit_type, Unset):
            raise ValueError(f"edit_type must match const 'add_column', got '{edit_type}'")

        dataset_add_column = cls(column_values=column_values, new_column_name=new_column_name, edit_type=edit_type)

        dataset_add_column.additional_properties = d
        return dataset_add_column

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
