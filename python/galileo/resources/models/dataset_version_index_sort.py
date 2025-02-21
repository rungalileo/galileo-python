from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetVersionIndexSort")


@_attrs_define
class DatasetVersionIndexSort:
    """
    Attributes:
        ascending (Union[Unset, bool]):  Default: True.
        name (Union[Literal['version_index'], Unset]):  Default: 'version_index'.
        sort_type (Union[Literal['column'], Unset]):  Default: 'column'.
    """

    ascending: Union[Unset, bool] = True
    name: Union[Literal["version_index"], Unset] = "version_index"
    sort_type: Union[Literal["column"], Unset] = "column"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ascending = self.ascending

        name = self.name

        sort_type = self.sort_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ascending is not UNSET:
            field_dict["ascending"] = ascending
        if name is not UNSET:
            field_dict["name"] = name
        if sort_type is not UNSET:
            field_dict["sort_type"] = sort_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        ascending = d.pop("ascending", UNSET)

        name = cast(Union[Literal["version_index"], Unset], d.pop("name", UNSET))
        if name != "version_index" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'version_index', got '{name}'")

        sort_type = cast(Union[Literal["column"], Unset], d.pop("sort_type", UNSET))
        if sort_type != "column" and not isinstance(sort_type, Unset):
            raise ValueError(f"sort_type must match const 'column', got '{sort_type}'")

        dataset_version_index_sort = cls(ascending=ascending, name=name, sort_type=sort_type)

        dataset_version_index_sort.additional_properties = d
        return dataset_version_index_sort

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
