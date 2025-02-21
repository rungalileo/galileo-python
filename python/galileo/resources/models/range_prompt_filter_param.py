from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RangePromptFilterParam")


@_attrs_define
class RangePromptFilterParam:
    """
    Attributes:
        column (str):
        filter_type (Literal['range']):
        high (float):
        low (float):
    """

    column: str
    filter_type: Literal["range"]
    high: float
    low: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column = self.column

        filter_type = self.filter_type

        high = self.high

        low = self.low

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"column": column, "filter_type": filter_type, "high": high, "low": low})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        column = d.pop("column")

        filter_type = cast(Literal["range"], d.pop("filter_type"))
        if filter_type != "range":
            raise ValueError(f"filter_type must match const 'range', got '{filter_type}'")

        high = d.pop("high")

        low = d.pop("low")

        range_prompt_filter_param = cls(column=column, filter_type=filter_type, high=high, low=low)

        range_prompt_filter_param.additional_properties = d
        return range_prompt_filter_param

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
