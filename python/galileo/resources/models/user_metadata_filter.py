from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_metadata_filter_operator import UserMetadataFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserMetadataFilter")


@_attrs_define
class UserMetadataFilter:
    """
    Attributes:
        key (str):
        operator (UserMetadataFilterOperator):
        value (Union[list[str], str]):
        name (Union[Literal['user_metadata'], Unset]):  Default: 'user_metadata'.
    """

    key: str
    operator: UserMetadataFilterOperator
    value: Union[list[str], str]
    name: Union[Literal["user_metadata"], Unset] = "user_metadata"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        operator = self.operator.value

        value: Union[list[str], str]
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"key": key, "operator": operator, "value": value})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        operator = UserMetadataFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[list[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = cast(list[str], data)

                return value_type_1
            except:  # noqa: E722
                pass
            return cast(Union[list[str], str], data)

        value = _parse_value(d.pop("value"))

        name = cast(Union[Literal["user_metadata"], Unset], d.pop("name", UNSET))
        if name != "user_metadata" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'user_metadata', got '{name}'")

        user_metadata_filter = cls(key=key, operator=operator, value=value, name=name)

        user_metadata_filter.additional_properties = d
        return user_metadata_filter

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
