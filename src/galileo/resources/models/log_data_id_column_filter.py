from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogDataIDColumnFilter")


@_attrs_define
class LogDataIDColumnFilter:
    """
    Attributes:
        column_id (str):
        value (str):
        name (Union[Literal['id_column'], Unset]):  Default: 'id_column'.
    """

    column_id: str
    value: str
    name: Union[Literal["id_column"], Unset] = "id_column"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_id = self.column_id

        value = self.value

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"column_id": column_id, "value": value})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        column_id = d.pop("column_id")

        value = d.pop("value")

        name = cast(Union[Literal["id_column"], Unset], d.pop("name", UNSET))
        if name != "id_column" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'id_column', got '{name}'")

        log_data_id_column_filter = cls(column_id=column_id, value=value, name=name)

        log_data_id_column_filter.additional_properties = d
        return log_data_id_column_filter

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
