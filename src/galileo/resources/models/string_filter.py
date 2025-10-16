from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.string_filter_operator import StringFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="StringFilter")


@_attrs_define
class StringFilter:
    """Filters on a string field.

    Attributes
    ----------
        name (Union[None, str]):
        operator (StringFilterOperator):
        value (Union[list[str], str]):
        case_sensitive (Union[Unset, bool]):  Default: True.
    """

    name: Union[None, str]
    operator: StringFilterOperator
    value: Union[list[str], str]
    case_sensitive: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, str]
        name = self.name

        operator = self.operator.value

        value: Union[list[str], str]
        value = self.value if isinstance(self.value, list) else self.value

        case_sensitive = self.case_sensitive

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "operator": operator, "value": value})
        if case_sensitive is not UNSET:
            field_dict["case_sensitive"] = case_sensitive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        operator = StringFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[list[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[list[str], str], data)

        value = _parse_value(d.pop("value"))

        case_sensitive = d.pop("case_sensitive", UNSET)

        string_filter = cls(name=name, operator=operator, value=value, case_sensitive=case_sensitive)

        string_filter.additional_properties = d
        return string_filter

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
