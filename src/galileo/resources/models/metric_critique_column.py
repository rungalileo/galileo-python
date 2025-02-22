from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MetricCritiqueColumn")


@_attrs_define
class MetricCritiqueColumn:
    """
    Attributes:
        col_name (str):
        metric_critique_computing (bool):
    """

    col_name: str
    metric_critique_computing: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        col_name = self.col_name

        metric_critique_computing = self.metric_critique_computing

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"col_name": col_name, "metric_critique_computing": metric_critique_computing})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        col_name = d.pop("col_name")

        metric_critique_computing = d.pop("metric_critique_computing")

        metric_critique_column = cls(col_name=col_name, metric_critique_computing=metric_critique_computing)

        metric_critique_column.additional_properties = d
        return metric_critique_column

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
