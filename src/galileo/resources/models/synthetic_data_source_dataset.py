from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyntheticDataSourceDataset")


@_attrs_define
class SyntheticDataSourceDataset:
    """Configuration for dataset examples in synthetic data generation.

    Attributes:
        dataset_id (str):
        dataset_version_index (Union[None, Unset, int]):
        row_ids (Union[None, Unset, list[str]]):
    """

    dataset_id: str
    dataset_version_index: Union[None, Unset, int] = UNSET
    row_ids: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataset_id = self.dataset_id

        dataset_version_index: Union[None, Unset, int]
        if isinstance(self.dataset_version_index, Unset):
            dataset_version_index = UNSET
        else:
            dataset_version_index = self.dataset_version_index

        row_ids: Union[None, Unset, list[str]]
        if isinstance(self.row_ids, Unset):
            row_ids = UNSET
        elif isinstance(self.row_ids, list):
            row_ids = self.row_ids

        else:
            row_ids = self.row_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"dataset_id": dataset_id})
        if dataset_version_index is not UNSET:
            field_dict["dataset_version_index"] = dataset_version_index
        if row_ids is not UNSET:
            field_dict["row_ids"] = row_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dataset_id = d.pop("dataset_id")

        def _parse_dataset_version_index(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        dataset_version_index = _parse_dataset_version_index(d.pop("dataset_version_index", UNSET))

        def _parse_row_ids(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                row_ids_type_0 = cast(list[str], data)

                return row_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        row_ids = _parse_row_ids(d.pop("row_ids", UNSET))

        synthetic_data_source_dataset = cls(
            dataset_id=dataset_id, dataset_version_index=dataset_version_index, row_ids=row_ids
        )

        synthetic_data_source_dataset.additional_properties = d
        return synthetic_data_source_dataset

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
