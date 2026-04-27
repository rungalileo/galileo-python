from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AnnotationQueueNumAnnotatorsSort")


@_attrs_define
class AnnotationQueueNumAnnotatorsSort:
    """
    Attributes:
        name (Literal['num_annotators'] | Unset):  Default: 'num_annotators'.
        ascending (bool | Unset):  Default: True.
        sort_type (Literal['column'] | Unset):  Default: 'column'.
    """

    name: Literal["num_annotators"] | Unset = "num_annotators"
    ascending: bool | Unset = True
    sort_type: Literal["column"] | Unset = "column"
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
        name = cast(Literal["num_annotators"] | Unset, d.pop("name", UNSET))
        if name != "num_annotators" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'num_annotators', got '{name}'")

        ascending = d.pop("ascending", UNSET)

        sort_type = cast(Literal["column"] | Unset, d.pop("sort_type", UNSET))
        if sort_type != "column" and not isinstance(sort_type, Unset):
            raise ValueError(f"sort_type must match const 'column', got '{sort_type}'")

        annotation_queue_num_annotators_sort = cls(name=name, ascending=ascending, sort_type=sort_type)

        annotation_queue_num_annotators_sort.additional_properties = d
        return annotation_queue_num_annotators_sort

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
