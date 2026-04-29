from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_created_by_filter_operator import RunCreatedByFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="RunCreatedByFilter")


@_attrs_define
class RunCreatedByFilter:
    """
    Attributes
    ----------
        value (Union[list[str], str]):
        name (Union[Literal['created_by'], Unset]):  Default: 'created_by'.
        operator (Union[Unset, RunCreatedByFilterOperator]):  Default: RunCreatedByFilterOperator.EQ.
    """

    value: Union[list[str], str]
    name: Union[Literal["created_by"], Unset] = "created_by"
    operator: Union[Unset, RunCreatedByFilterOperator] = RunCreatedByFilterOperator.EQ
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value: Union[list[str], str]
        if isinstance(self.value, list):
            value = []
            for value_type_1_item_data in self.value:
                value_type_1_item: str
                value_type_1_item = value_type_1_item_data
                value.append(value_type_1_item)

        else:
            value = self.value

        name = self.name

        operator: Union[Unset, str] = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if name is not UNSET:
            field_dict["name"] = name
        if operator is not UNSET:
            field_dict["operator"] = operator

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_value(data: object) -> Union[list[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = []
                _value_type_1 = data
                for value_type_1_item_data in _value_type_1:

                    def _parse_value_type_1_item(data: object) -> str:
                        return cast(str, data)

                    value_type_1_item = _parse_value_type_1_item(value_type_1_item_data)

                    value_type_1.append(value_type_1_item)

                return value_type_1
            except:  # noqa: E722
                pass
            return cast(Union[list[str], str], data)

        value = _parse_value(d.pop("value"))

        name = cast(Union[Literal["created_by"], Unset], d.pop("name", UNSET))
        if name != "created_by" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'created_by', got '{name}'")

        _operator = d.pop("operator", UNSET)
        operator: Union[Unset, RunCreatedByFilterOperator]
        operator = UNSET if isinstance(_operator, Unset) else RunCreatedByFilterOperator(_operator)

        run_created_by_filter = cls(value=value, name=name, operator=operator)

        run_created_by_filter.additional_properties = d
        return run_created_by_filter

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
