from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogRecordsBooleanFilter")


@_attrs_define
class LogRecordsBooleanFilter:
    """
    Attributes:
        column_id (str): ID of the column to filter.
        value (bool):
        type_ (Union[Literal['boolean'], Unset]):  Default: 'boolean'.
    """

    column_id: str
    value: bool
    type_: Union[Literal["boolean"], Unset] = "boolean"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_id = self.column_id

        value = self.value

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"column_id": column_id, "value": value})
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        column_id = d.pop("column_id")

        value = d.pop("value")

        type_ = cast(Union[Literal["boolean"], Unset], d.pop("type", UNSET))
        if type_ != "boolean" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'boolean', got '{type_}'")

        log_records_boolean_filter = cls(column_id=column_id, value=value, type_=type_)

        log_records_boolean_filter.additional_properties = d
        return log_records_boolean_filter

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
