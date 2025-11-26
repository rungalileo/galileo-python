from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetUpdatedAtSort")


@_attrs_define
class DatasetUpdatedAtSort:
    """
    Attributes
    ----------
        name (Union[Literal['updated_at'], Unset]):  Default: 'updated_at'.
        ascending (Union[Unset, bool]):  Default: True.
        sort_type (Union[Literal['column'], Unset]):  Default: 'column'.
    """

    name: Union[Literal["updated_at"], Unset] = "updated_at"
    ascending: Union[Unset, bool] = True
    sort_type: Union[Literal["column"], Unset] = "column"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        ascending = self.ascending

        sort_type = self.sort_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if ascending is not UNSET:
            field_dict["ascending"] = ascending
        if sort_type is not UNSET:
            field_dict["sort_type"] = sort_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = cast(Union[Literal["updated_at"], Unset], d.pop("name", UNSET))
        if name != "updated_at" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'updated_at', got '{name}'")

        ascending = d.pop("ascending", UNSET)

        sort_type = cast(Union[Literal["column"], Unset], d.pop("sort_type", UNSET))
        if sort_type != "column" and not isinstance(sort_type, Unset):
            raise ValueError(f"sort_type must match const 'column', got '{sort_type}'")

        dataset_updated_at_sort = cls(name=name, ascending=ascending, sort_type=sort_type)

        dataset_updated_at_sort.additional_properties = d
        return dataset_updated_at_sort

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
