from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.operator import Operator
from ..types import UNSET, Unset

T = TypeVar("T", bound="RawFilter")


@_attrs_define
class RawFilter:
    """Raw filter input. At least one of 'name' or 'column_id' is required.
    'value' is required. 'operator' and 'case_sensitive' are optional.

    Attributes
    ----------
            value (Any):
            name (Union[None, Unset, str]):
            column_id (Union[None, Unset, str]):
            operator (Union[None, Operator, Unset]):
            case_sensitive (Union[None, Unset, bool]):
    """

    value: Any
    name: Union[None, Unset, str] = UNSET
    column_id: Union[None, Unset, str] = UNSET
    operator: Union[None, Operator, Unset] = UNSET
    case_sensitive: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        name: Union[None, Unset, str]
        name = UNSET if isinstance(self.name, Unset) else self.name

        column_id: Union[None, Unset, str]
        column_id = UNSET if isinstance(self.column_id, Unset) else self.column_id

        operator: Union[None, Unset, str]
        if isinstance(self.operator, Unset):
            operator = UNSET
        elif isinstance(self.operator, Operator):
            operator = self.operator.value
        else:
            operator = self.operator

        case_sensitive: Union[None, Unset, bool]
        case_sensitive = UNSET if isinstance(self.case_sensitive, Unset) else self.case_sensitive

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if name is not UNSET:
            field_dict["name"] = name
        if column_id is not UNSET:
            field_dict["column_id"] = column_id
        if operator is not UNSET:
            field_dict["operator"] = operator
        if case_sensitive is not UNSET:
            field_dict["case_sensitive"] = case_sensitive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_column_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        column_id = _parse_column_id(d.pop("column_id", UNSET))

        def _parse_operator(data: object) -> Union[None, Operator, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return Operator(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Operator, Unset], data)

        operator = _parse_operator(d.pop("operator", UNSET))

        def _parse_case_sensitive(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        case_sensitive = _parse_case_sensitive(d.pop("case_sensitive", UNSET))

        raw_filter = cls(value=value, name=name, column_id=column_id, operator=operator, case_sensitive=case_sensitive)

        raw_filter.additional_properties = d
        return raw_filter

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
