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
        index (int):
        values (DatasetUpdateRowValues):
        edit_type (Union[Literal['update_row'], Unset]):  Default: 'update_row'.
    """

    index: int
    values: "DatasetUpdateRowValues"
    edit_type: Union[Literal["update_row"], Unset] = "update_row"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index = self.index

        values = self.values.to_dict()

        edit_type = self.edit_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"index": index, "values": values})
        if edit_type is not UNSET:
            field_dict["edit_type"] = edit_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dataset_update_row_values import DatasetUpdateRowValues

        d = src_dict.copy()
        index = d.pop("index")

        values = DatasetUpdateRowValues.from_dict(d.pop("values"))

        edit_type = cast(Union[Literal["update_row"], Unset], d.pop("edit_type", UNSET))
        if edit_type != "update_row" and not isinstance(edit_type, Unset):
            raise ValueError(f"edit_type must match const 'update_row', got '{edit_type}'")

        dataset_update_row = cls(index=index, values=values, edit_type=edit_type)

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
