from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PromptDatasetDB")


@_attrs_define
class PromptDatasetDB:
    """
    Attributes:
        dataset_id (str):
        id (str):
        file_name (Union[None, Unset, str]):
        message (Union[None, Unset, str]):
        num_rows (Union[None, Unset, int]):
        rows (Union[None, Unset, int]):
    """

    dataset_id: str
    id: str
    file_name: Union[None, Unset, str] = UNSET
    message: Union[None, Unset, str] = UNSET
    num_rows: Union[None, Unset, int] = UNSET
    rows: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataset_id = self.dataset_id

        id = self.id

        file_name: Union[None, Unset, str]
        if isinstance(self.file_name, Unset):
            file_name = UNSET
        else:
            file_name = self.file_name

        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        num_rows: Union[None, Unset, int]
        if isinstance(self.num_rows, Unset):
            num_rows = UNSET
        else:
            num_rows = self.num_rows

        rows: Union[None, Unset, int]
        if isinstance(self.rows, Unset):
            rows = UNSET
        else:
            rows = self.rows

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"dataset_id": dataset_id, "id": id})
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        dataset_id = d.pop("dataset_id")

        id = d.pop("id")

        def _parse_file_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        file_name = _parse_file_name(d.pop("file_name", UNSET))

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_num_rows(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_rows = _parse_num_rows(d.pop("num_rows", UNSET))

        def _parse_rows(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        rows = _parse_rows(d.pop("rows", UNSET))

        prompt_dataset_db = cls(
            dataset_id=dataset_id, id=id, file_name=file_name, message=message, num_rows=num_rows, rows=rows
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
