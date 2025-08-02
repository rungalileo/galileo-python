from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dataset_id_filter_operator import DatasetIDFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetIDFilter")


@_attrs_define
class DatasetIDFilter:
    """
    Attributes:
        value (str):
        name (Union[Literal['id'], Unset]):  Default: 'id'.
        operator (Union[Unset, DatasetIDFilterOperator]):  Default: DatasetIDFilterOperator.EQ.
    """

    value: str
    name: Union[Literal["id"], Unset] = "id"
    operator: Union[Unset, DatasetIDFilterOperator] = DatasetIDFilterOperator.EQ
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        name = self.name

        operator: Union[Unset, str] = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if name is not UNSET:
            field_dict["name"] = name
        if operator is not UNSET:
            field_dict["operator"] = operator

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        name = cast(Union[Literal["id"], Unset], d.pop("name", UNSET))
        if name != "id" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'id', got '{name}'")

        _operator = d.pop("operator", UNSET)
        operator: Union[Unset, DatasetIDFilterOperator]
        if isinstance(_operator, Unset):
            operator = UNSET
        else:
            operator = DatasetIDFilterOperator(_operator)

        dataset_id_filter = cls(value=value, name=name, operator=operator)

        dataset_id_filter.additional_properties = d
        return dataset_id_filter

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
