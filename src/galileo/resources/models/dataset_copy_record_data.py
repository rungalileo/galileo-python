from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetCopyRecordData")


@_attrs_define
class DatasetCopyRecordData:
    """Prepend or append trace or span data to dataset.

    Attributes
    ----------
        project_id (str):
        ids (list[str]): List of trace or span IDs to copy data from
        edit_type (Union[Literal['copy_record_data'], Unset]):  Default: 'copy_record_data'.
        prepend (Union[Unset, bool]): A flag to control appending vs prepending Default: True.
    """

    project_id: str
    ids: list[str]
    edit_type: Union[Literal["copy_record_data"], Unset] = "copy_record_data"
    prepend: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        ids = self.ids

        edit_type = self.edit_type

        prepend = self.prepend

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "ids": ids})
        if edit_type is not UNSET:
            field_dict["edit_type"] = edit_type
        if prepend is not UNSET:
            field_dict["prepend"] = prepend

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        ids = cast(list[str], d.pop("ids"))

        edit_type = cast(Union[Literal["copy_record_data"], Unset], d.pop("edit_type", UNSET))
        if edit_type != "copy_record_data" and not isinstance(edit_type, Unset):
            raise ValueError(f"edit_type must match const 'copy_record_data', got '{edit_type}'")

        prepend = d.pop("prepend", UNSET)

        dataset_copy_record_data = cls(project_id=project_id, ids=ids, edit_type=edit_type, prepend=prepend)

        dataset_copy_record_data.additional_properties = d
        return dataset_copy_record_data

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
