from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetDeleteColumn")


@_attrs_define
class DatasetDeleteColumn:
    """
    Attributes:
        column_name (str):
        edit_type (Union[Literal['delete_column'], Unset]):  Default: 'delete_column'.
    """

    column_name: str
    edit_type: Union[Literal["delete_column"], Unset] = "delete_column"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_name = self.column_name

        edit_type = self.edit_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"column_name": column_name})
        if edit_type is not UNSET:
            field_dict["edit_type"] = edit_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        column_name = d.pop("column_name")

        edit_type = cast(Union[Literal["delete_column"], Unset], d.pop("edit_type", UNSET))
        if edit_type != "delete_column" and not isinstance(edit_type, Unset):
            raise ValueError(f"edit_type must match const 'delete_column', got '{edit_type}'")

        dataset_delete_column = cls(column_name=column_name, edit_type=edit_type)

        dataset_delete_column.additional_properties = d
        return dataset_delete_column

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
