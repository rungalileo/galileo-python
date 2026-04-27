from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_last_name_filter_operator import UserLastNameFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserLastNameFilter")


@_attrs_define
class UserLastNameFilter:
    """
    Attributes:
        operator (UserLastNameFilterOperator):
        value (list[str] | str):
        name (Literal['last_name'] | Unset):  Default: 'last_name'.
        case_sensitive (bool | Unset):  Default: True.
    """

    operator: UserLastNameFilterOperator
    value: list[str] | str
    name: Literal["last_name"] | Unset = "last_name"
    case_sensitive: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value: list[str] | str
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        name = self.name

        case_sensitive = self.case_sensitive

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operator": operator, "value": value})
        if name is not UNSET:
            field_dict["name"] = name
        if case_sensitive is not UNSET:
            field_dict["case_sensitive"] = case_sensitive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operator = UserLastNameFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> list[str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = cast(list[str], data)

                return value_type_1
            except:  # noqa: E722
                pass
            return cast(list[str] | str, data)

        value = _parse_value(d.pop("value"))

        name = cast(Literal["last_name"] | Unset, d.pop("name", UNSET))
        if name != "last_name" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'last_name', got '{name}'")

        case_sensitive = d.pop("case_sensitive", UNSET)

        user_last_name_filter = cls(operator=operator, value=value, name=name, case_sensitive=case_sensitive)

        user_last_name_filter.additional_properties = d
        return user_last_name_filter

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
