from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_number_filter_operator import CustomNumberFilterOperator

T = TypeVar("T", bound="CustomNumberFilter")


@_attrs_define
class CustomNumberFilter:
    """
    Attributes:
        name (Union[None, str]):
        operator (CustomNumberFilterOperator):
        value (Union[float, int, list[float], list[int]]):
    """

    name: Union[None, str]
    operator: CustomNumberFilterOperator
    value: Union[float, int, list[float], list[int]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, str]
        name = self.name

        operator = self.operator.value

        value: Union[float, int, list[float], list[int]]
        value = self.value if isinstance(self.value, (list, list)) else self.value

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

        operator = CustomNumberFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[float, int, list[float], list[int]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[int], data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[float], data)

            except:  # noqa: E722
                pass
            return cast(Union[float, int, list[float], list[int]], data)

        value = _parse_value(d.pop("value"))

        custom_number_filter = cls(name=name, operator=operator, value=value)

        custom_number_filter.additional_properties = d
        return custom_number_filter

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
