from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectBookmarkSort")


@_attrs_define
class ProjectBookmarkSort:
    """
    Attributes:
        ascending (Union[Unset, bool]):  Default: True.
        name (Union[Literal['bookmark'], Unset]):  Default: 'bookmark'.
        sort_type (Union[Literal['custom'], Unset]):  Default: 'custom'.
    """

    ascending: Union[Unset, bool] = True
    name: Union[Literal["bookmark"], Unset] = "bookmark"
    sort_type: Union[Literal["custom"], Unset] = "custom"
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

        name = cast(Union[Literal["bookmark"], Unset], d.pop("name", UNSET))
        if name != "bookmark" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'bookmark', got '{name}'")

        sort_type = cast(Union[Literal["custom"], Unset], d.pop("sort_type", UNSET))
        if sort_type != "custom" and not isinstance(sort_type, Unset):
            raise ValueError(f"sort_type must match const 'custom', got '{sort_type}'")

        project_bookmark_sort = cls(ascending=ascending, name=name, sort_type=sort_type)

        project_bookmark_sort.additional_properties = d
        return project_bookmark_sort

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
