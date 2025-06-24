from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.log_records_number_filter_operator import LogRecordsNumberFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="LogRecordsNumberFilter")


@_attrs_define
class LogRecordsNumberFilter:
    """
    Attributes:
        column_id (str): ID of the column to filter.
        operator (LogRecordsNumberFilterOperator):
        value (Union[float, int, list[float], list[int]]):
        type_ (Union[Literal['number'], Unset]):  Default: 'number'.
    """

    column_id: str
    operator: LogRecordsNumberFilterOperator
    value: Union[float, int, list[float], list[int]]
    type_: Union[Literal["number"], Unset] = "number"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_id = self.column_id

        operator = self.operator.value

        value: Union[float, int, list[float], list[int]]
        if isinstance(self.value, list):
            value = self.value

        elif isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"column_id": column_id, "operator": operator, "value": value})
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        column_id = d.pop("column_id")

        operator = LogRecordsNumberFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[float, int, list[float], list[int]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_2 = cast(list[int], data)

                return value_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_3 = cast(list[float], data)

                return value_type_3
            except:  # noqa: E722
                pass
            return cast(Union[float, int, list[float], list[int]], data)

        value = _parse_value(d.pop("value"))

        type_ = cast(Union[Literal["number"], Unset], d.pop("type", UNSET))
        if type_ != "number" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'number', got '{type_}'")

        log_records_number_filter = cls(column_id=column_id, operator=operator, value=value, type_=type_)

        log_records_number_filter.additional_properties = d
        return log_records_number_filter

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
