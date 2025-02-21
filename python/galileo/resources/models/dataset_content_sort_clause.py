from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetContentSortClause")


@_attrs_define
class DatasetContentSortClause:
    """
    Attributes:
        column_name (str):
        ascending (Union[Unset, bool]):  Default: True.
    """

    column_name: str
    ascending: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_name = self.column_name

        ascending = self.ascending

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"column_name": column_name})
        if ascending is not UNSET:
            field_dict["ascending"] = ascending

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        column_name = d.pop("column_name")

        ascending = d.pop("ascending", UNSET)

        dataset_content_sort_clause = cls(column_name=column_name, ascending=ascending)

        dataset_content_sort_clause.additional_properties = d
        return dataset_content_sort_clause

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
