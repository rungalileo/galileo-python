from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.log_records_text_filter_operator import LogRecordsTextFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="LogRecordsTextFilter")


@_attrs_define
class LogRecordsTextFilter:
    """
    Attributes:
        column_id (str): ID of the column to filter.
        operator (LogRecordsTextFilterOperator):
        value (Union[list[str], str]):
        case_sensitive (Union[Unset, bool]):  Default: True.
        type_ (Union[Literal['text'], Unset]):  Default: 'text'.
    """

    column_id: str
    operator: LogRecordsTextFilterOperator
    value: Union[list[str], str]
    case_sensitive: Union[Unset, bool] = True
    type_: Union[Literal["text"], Unset] = "text"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_id = self.column_id

        operator = self.operator.value

        value: Union[list[str], str]
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        case_sensitive = self.case_sensitive

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"column_id": column_id, "operator": operator, "value": value})
        if case_sensitive is not UNSET:
            field_dict["case_sensitive"] = case_sensitive
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        column_id = d.pop("column_id")

        operator = LogRecordsTextFilterOperator(d.pop("operator"))

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

        case_sensitive = d.pop("case_sensitive", UNSET)

        type_ = cast(Union[Literal["text"], Unset], d.pop("type", UNSET))
        if type_ != "text" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'text', got '{type_}'")

        log_records_text_filter = cls(
            column_id=column_id, operator=operator, value=value, case_sensitive=case_sensitive, type_=type_
        )

        log_records_text_filter.additional_properties = d
        return log_records_text_filter

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
