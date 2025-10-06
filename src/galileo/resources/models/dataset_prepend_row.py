from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_prepend_row_values import DatasetPrependRowValues


T = TypeVar("T", bound="DatasetPrependRow")


@_attrs_define
class DatasetPrependRow:
    """
    Attributes:
        values (DatasetPrependRowValues):
        edit_type (Union[Literal['prepend_row'], Unset]):  Default: 'prepend_row'.
        row_id (Union[None, Unset, str]):
    """

    values: "DatasetPrependRowValues"
    edit_type: Union[Literal["prepend_row"], Unset] = "prepend_row"
    row_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        values = self.values.to_dict()

        edit_type = self.edit_type

        row_id: Union[None, Unset, str]
        row_id = UNSET if isinstance(self.row_id, Unset) else self.row_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"values": values})
        if edit_type is not UNSET:
            field_dict["edit_type"] = edit_type
        if row_id is not UNSET:
            field_dict["row_id"] = row_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_prepend_row_values import DatasetPrependRowValues

        d = dict(src_dict)
        values = DatasetPrependRowValues.from_dict(d.pop("values"))

        edit_type = cast(Union[Literal["prepend_row"], Unset], d.pop("edit_type", UNSET))
        if edit_type != "prepend_row" and not isinstance(edit_type, Unset):
            raise ValueError(f"edit_type must match const 'prepend_row', got '{edit_type}'")

        def _parse_row_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        row_id = _parse_row_id(d.pop("row_id", UNSET))

        dataset_prepend_row = cls(values=values, edit_type=edit_type, row_id=row_id)

        dataset_prepend_row.additional_properties = d
        return dataset_prepend_row

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
