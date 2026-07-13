from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetRemoveColumn")


@_attrs_define
class DatasetRemoveColumn:
    """Drop a column from the dataset schema.

    Attributes
    ----------
        column_name (str):
        edit_type (Union[Literal['remove_column'], Unset]):  Default: 'remove_column'.
    """

    column_name: str
    edit_type: Literal["remove_column"] | Unset = "remove_column"
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        column_name = d.pop("column_name")

        edit_type = cast(Literal["remove_column"] | Unset, d.pop("edit_type", UNSET))
        if edit_type != "remove_column" and not isinstance(edit_type, Unset):
            raise ValueError(f"edit_type must match const 'remove_column', got '{edit_type}'")

        dataset_remove_column = cls(column_name=column_name, edit_type=edit_type)

        dataset_remove_column.additional_properties = d
        return dataset_remove_column

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
