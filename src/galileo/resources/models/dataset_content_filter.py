from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dataset_content_filter_operator import DatasetContentFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetContentFilter")


@_attrs_define
class DatasetContentFilter:
    """
    Attributes:
        column_name (str):
        value (str):
        operator (Union[Unset, DatasetContentFilterOperator]):
    """

    column_name: str
    value: str
    operator: Union[Unset, DatasetContentFilterOperator] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_name = self.column_name

        value = self.value

        operator: Union[Unset, str] = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"column_name": column_name, "value": value})
        if operator is not UNSET:
            field_dict["operator"] = operator

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        column_name = d.pop("column_name")

        value = d.pop("value")

        _operator = d.pop("operator", UNSET)
        operator: Union[Unset, DatasetContentFilterOperator]
        if isinstance(_operator, Unset):
            operator = UNSET
        else:
            operator = DatasetContentFilterOperator(_operator)

        dataset_content_filter = cls(column_name=column_name, value=value, operator=operator)

        dataset_content_filter.additional_properties = d
        return dataset_content_filter

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
