from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metric_critique_column import MetricCritiqueColumn


T = TypeVar("T", bound="MetricCritiqueColumns")


@_attrs_define
class MetricCritiqueColumns:
    """
    Attributes:
        metric_critique_columns (list['MetricCritiqueColumn']):
    """

    metric_critique_columns: list["MetricCritiqueColumn"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric_critique_columns = []
        for metric_critique_columns_item_data in self.metric_critique_columns:
            metric_critique_columns_item = metric_critique_columns_item_data.to_dict()
            metric_critique_columns.append(metric_critique_columns_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"metric_critique_columns": metric_critique_columns})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric_critique_column import MetricCritiqueColumn

        d = src_dict.copy()
        metric_critique_columns = []
        _metric_critique_columns = d.pop("metric_critique_columns")
        for metric_critique_columns_item_data in _metric_critique_columns:
            metric_critique_columns_item = MetricCritiqueColumn.from_dict(metric_critique_columns_item_data)

            metric_critique_columns.append(metric_critique_columns_item)

        metric_critique_columns = cls(metric_critique_columns=metric_critique_columns)

        metric_critique_columns.additional_properties = d
        return metric_critique_columns

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
