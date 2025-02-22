from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetProjectLastUsedAtSort")


@_attrs_define
class DatasetProjectLastUsedAtSort:
    """
    Attributes:
        value (str):
        ascending (Union[Unset, bool]):  Default: True.
        name (Union[Literal['project_last_used_at'], Unset]):  Default: 'project_last_used_at'.
        sort_type (Union[Literal['custom_uuid'], Unset]):  Default: 'custom_uuid'.
    """

    value: str
    ascending: Union[Unset, bool] = True
    name: Union[Literal["project_last_used_at"], Unset] = "project_last_used_at"
    sort_type: Union[Literal["custom_uuid"], Unset] = "custom_uuid"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        ascending = self.ascending

        name = self.name

        sort_type = self.sort_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
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
        value = d.pop("value")

        ascending = d.pop("ascending", UNSET)

        name = cast(Union[Literal["project_last_used_at"], Unset], d.pop("name", UNSET))
        if name != "project_last_used_at" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'project_last_used_at', got '{name}'")

        sort_type = cast(Union[Literal["custom_uuid"], Unset], d.pop("sort_type", UNSET))
        if sort_type != "custom_uuid" and not isinstance(sort_type, Unset):
            raise ValueError(f"sort_type must match const 'custom_uuid', got '{sort_type}'")

        dataset_project_last_used_at_sort = cls(value=value, ascending=ascending, name=name, sort_type=sort_type)

        dataset_project_last_used_at_sort.additional_properties = d
        return dataset_project_last_used_at_sort

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
