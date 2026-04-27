from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PromptDatasetDB")


@_attrs_define
class PromptDatasetDB:
    """
    Attributes:
        id (str):
        dataset_id (str):
        file_name (None | str | Unset):
        message (None | str | Unset):
        num_rows (int | None | Unset):
        rows (int | None | Unset):
    """

    id: str
    dataset_id: str
    file_name: None | str | Unset = UNSET
    message: None | str | Unset = UNSET
    num_rows: int | None | Unset = UNSET
    rows: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        dataset_id = self.dataset_id

        file_name: None | str | Unset
        if isinstance(self.file_name, Unset):
            file_name = UNSET
        else:
            file_name = self.file_name

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        num_rows: int | None | Unset
        if isinstance(self.num_rows, Unset):
            num_rows = UNSET
        else:
            num_rows = self.num_rows

        rows: int | None | Unset
        if isinstance(self.rows, Unset):
            rows = UNSET
        else:
            rows = self.rows

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "dataset_id": dataset_id})
        if file_name is not UNSET:
            field_dict["file_name"] = file_name
        if message is not UNSET:
            field_dict["message"] = message
        if num_rows is not UNSET:
            field_dict["num_rows"] = num_rows
        if rows is not UNSET:
            field_dict["rows"] = rows

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        dataset_id = d.pop("dataset_id")

        def _parse_file_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_name = _parse_file_name(d.pop("file_name", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_num_rows(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_rows = _parse_num_rows(d.pop("num_rows", UNSET))

        def _parse_rows(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        rows = _parse_rows(d.pop("rows", UNSET))

        prompt_dataset_db = cls(
            id=id, dataset_id=dataset_id, file_name=file_name, message=message, num_rows=num_rows, rows=rows
        )

        prompt_dataset_db.additional_properties = d
        return prompt_dataset_db

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
