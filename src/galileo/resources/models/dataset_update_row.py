from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_update_row_values import DatasetUpdateRowValues


T = TypeVar("T", bound="DatasetUpdateRow")


@_attrs_define
class DatasetUpdateRow:
    """
    Attributes:
        values (DatasetUpdateRowValues):
        edit_type (Union[Literal['update_row'], Unset]):  Default: 'update_row'.
        index (Union[None, Unset, int]):
        row_id (Union[None, Unset, str]):
    """

    values: "DatasetUpdateRowValues"
    edit_type: Union[Literal["update_row"], Unset] = "update_row"
    index: Union[None, Unset, int] = UNSET
    row_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        values = self.values.to_dict()

        edit_type = self.edit_type

        index: Union[None, Unset, int]
        if isinstance(self.index, Unset):
            index = UNSET
        else:
            index = self.index

        row_id: Union[None, Unset, str]
        if isinstance(self.row_id, Unset):
            row_id = UNSET
        else:
            row_id = self.row_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"values": values})
        if edit_type is not UNSET:
            field_dict["edit_type"] = edit_type
        if index is not UNSET:
            field_dict["index"] = index
        if row_id is not UNSET:
            field_dict["row_id"] = row_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_update_row_values import DatasetUpdateRowValues

        d = dict(src_dict)
        values = DatasetUpdateRowValues.from_dict(d.pop("values"))

        edit_type = cast(Union[Literal["update_row"], Unset], d.pop("edit_type", UNSET))
        if edit_type != "update_row" and not isinstance(edit_type, Unset):
            raise ValueError(f"edit_type must match const 'update_row', got '{edit_type}'")

        def _parse_index(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        index = _parse_index(d.pop("index", UNSET))

        def _parse_row_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        row_id = _parse_row_id(d.pop("row_id", UNSET))

        dataset_update_row = cls(values=values, edit_type=edit_type, index=index, row_id=row_id)

        dataset_update_row.additional_properties = d
        return dataset_update_row

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
