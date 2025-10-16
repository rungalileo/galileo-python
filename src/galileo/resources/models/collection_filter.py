from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.collection_filter_operator import CollectionFilterOperator

T = TypeVar("T", bound="CollectionFilter")


@_attrs_define
class CollectionFilter:
    """Filters for string items in a collection/list.

    Attributes
    ----------
        name (Union[None, str]):
        operator (CollectionFilterOperator):
        value (str):
    """

    name: Union[None, str]
    operator: CollectionFilterOperator
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, str]
        name = self.name

        operator = self.operator.value

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "operator": operator, "value": value})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        operator = CollectionFilterOperator(d.pop("operator"))

        value = d.pop("value")

        collection_filter = cls(name=name, operator=operator, value=value)

        collection_filter.additional_properties = d
        return collection_filter

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
