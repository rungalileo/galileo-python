from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BarChart")


@_attrs_define
class BarChart:
    """A class to represent a basic bar chart.

    labels: List[str] the x axis labels
    values: List[int | float] the counts for each bar

        Attributes:
            labels (list[str]):
            values (list[Union[float, int]]):
    """

    labels: list[str]
    values: list[Union[float, int]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        labels = self.labels

        values = []
        for values_item_data in self.values:
            values_item: Union[float, int]
            values_item = values_item_data
            values.append(values_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"labels": labels, "values": values})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        labels = cast(list[str], d.pop("labels"))

        values = []
        _values = d.pop("values")
        for values_item_data in _values:

            def _parse_values_item(data: object) -> Union[float, int]:
                return cast(Union[float, int], data)

            values_item = _parse_values_item(values_item_data)

            values.append(values_item)

        bar_chart = cls(labels=labels, values=values)

        bar_chart.additional_properties = d
        return bar_chart

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
