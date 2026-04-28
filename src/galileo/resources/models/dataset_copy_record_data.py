from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetCopyRecordData")


@_attrs_define
class DatasetCopyRecordData:
    """Prepend or append trace or span data to dataset.

    Attributes
    ----------
        ids (list[str]): List of trace or span IDs to copy data from
        edit_type (Literal['copy_record_data'] | Unset):  Default: 'copy_record_data'.
        project_id (None | str | Unset):
        queue_id (None | str | Unset):
        prepend (bool | Unset): A flag to control appending vs prepending Default: True.
        use_generated_output_column (bool | Unset): If True, write trace output to generated_output column; if False,
            write to output column (backward compatible) Default: False.
    """

    ids: list[str]
    edit_type: Literal["copy_record_data"] | Unset = "copy_record_data"
    project_id: None | str | Unset = UNSET
    queue_id: None | str | Unset = UNSET
    prepend: bool | Unset = True
    use_generated_output_column: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ids = self.ids

        edit_type = self.edit_type

        project_id: None | str | Unset
        project_id = UNSET if isinstance(self.project_id, Unset) else self.project_id

        queue_id: None | str | Unset
        queue_id = UNSET if isinstance(self.queue_id, Unset) else self.queue_id

        prepend = self.prepend

        use_generated_output_column = self.use_generated_output_column

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"ids": ids})
        if edit_type is not UNSET:
            field_dict["edit_type"] = edit_type
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if queue_id is not UNSET:
            field_dict["queue_id"] = queue_id
        if prepend is not UNSET:
            field_dict["prepend"] = prepend
        if use_generated_output_column is not UNSET:
            field_dict["use_generated_output_column"] = use_generated_output_column

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ids = cast(list[str], d.pop("ids"))

        edit_type = cast(Literal["copy_record_data"] | Unset, d.pop("edit_type", UNSET))
        if edit_type != "copy_record_data" and not isinstance(edit_type, Unset):
            raise ValueError(f"edit_type must match const 'copy_record_data', got '{edit_type}'")

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_queue_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        queue_id = _parse_queue_id(d.pop("queue_id", UNSET))

        prepend = d.pop("prepend", UNSET)

        use_generated_output_column = d.pop("use_generated_output_column", UNSET)

        dataset_copy_record_data = cls(
            ids=ids,
            edit_type=edit_type,
            project_id=project_id,
            queue_id=queue_id,
            prepend=prepend,
            use_generated_output_column=use_generated_output_column,
        )

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
