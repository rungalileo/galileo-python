from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpsertDatasetContentRequest")


@_attrs_define
class UpsertDatasetContentRequest:
    """
    Attributes:
        dataset_id (str): The ID of the dataset to copy content from.
        version_index (Union[None, Unset, int]): The version index of the dataset to copy content from. If not provided,
            the content will be copied from the latest version of the dataset.
    """

    dataset_id: str
    version_index: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataset_id = self.dataset_id

        version_index: Union[None, Unset, int]
        if isinstance(self.version_index, Unset):
            version_index = UNSET
        else:
            version_index = self.version_index

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"dataset_id": dataset_id})
        if version_index is not UNSET:
            field_dict["version_index"] = version_index

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dataset_id = d.pop("dataset_id")

        def _parse_version_index(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        version_index = _parse_version_index(d.pop("version_index", UNSET))

        upsert_dataset_content_request = cls(dataset_id=dataset_id, version_index=version_index)

        upsert_dataset_content_request.additional_properties = d
        return upsert_dataset_content_request

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
