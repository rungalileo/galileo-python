from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetDeleteRow")


@_attrs_define
class DatasetDeleteRow:
    """
    Attributes:
        row_id (str):
        edit_type (Union[Literal['delete_row'], Unset]):  Default: 'delete_row'.
    """

    row_id: str
    edit_type: Union[Literal["delete_row"], Unset] = "delete_row"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        row_id = self.row_id

        edit_type = self.edit_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"row_id": row_id})
        if edit_type is not UNSET:
            field_dict["edit_type"] = edit_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        row_id = d.pop("row_id")

        edit_type = cast(Union[Literal["delete_row"], Unset], d.pop("edit_type", UNSET))
        if edit_type != "delete_row" and not isinstance(edit_type, Unset):
            raise ValueError(f"edit_type must match const 'delete_row', got '{edit_type}'")

        dataset_delete_row = cls(row_id=row_id, edit_type=edit_type)

        dataset_delete_row.additional_properties = d
        return dataset_delete_row

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
