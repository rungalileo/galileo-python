from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.log_records_collection_filter_operator import LogRecordsCollectionFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="LogRecordsCollectionFilter")


@_attrs_define
class LogRecordsCollectionFilter:
    """
    Attributes
    ----------
        column_id (str): ID of the column to filter.
        operator (LogRecordsCollectionFilterOperator):
        value (Union[list[str], str]):
        case_sensitive (Union[Unset, bool]):  Default: True.
        type_ (Union[Literal['collection'], Unset]):  Default: 'collection'.
    """

    column_id: str
    operator: LogRecordsCollectionFilterOperator
    value: Union[list[str], str]
    case_sensitive: Union[Unset, bool] = True
    type_: Union[Literal["collection"], Unset] = "collection"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column_id = self.column_id

        operator = self.operator.value

        value: Union[list[str], str]
        value = self.value if isinstance(self.value, list) else self.value

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

        operator = LogRecordsCollectionFilterOperator(d.pop("operator"))

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

        type_ = cast(Union[Literal["collection"], Unset], d.pop("type", UNSET))
        if type_ != "collection" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'collection', got '{type_}'")

        log_records_collection_filter = cls(
            column_id=column_id, operator=operator, value=value, case_sensitive=case_sensitive, type_=type_
        )

        log_records_collection_filter.additional_properties = d
        return log_records_collection_filter

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
