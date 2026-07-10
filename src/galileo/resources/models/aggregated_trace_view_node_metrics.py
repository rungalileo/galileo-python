from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.categorical_metric_info import CategoricalMetricInfo
    from ..models.system_metric_info import SystemMetricInfo


T = TypeVar("T", bound="AggregatedTraceViewNodeMetrics")


@_attrs_define
class AggregatedTraceViewNodeMetrics:
    """ """

    additional_properties: dict[str, Union["CategoricalMetricInfo", "SystemMetricInfo"]] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.system_metric_info import SystemMetricInfo

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, SystemMetricInfo):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.categorical_metric_info import CategoricalMetricInfo
        from ..models.system_metric_info import SystemMetricInfo

        d = dict(src_dict)
        aggregated_trace_view_node_metrics = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Union["CategoricalMetricInfo", "SystemMetricInfo"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return SystemMetricInfo.from_dict(data)

                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                return CategoricalMetricInfo.from_dict(data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        aggregated_trace_view_node_metrics.additional_properties = additional_properties
        return aggregated_trace_view_node_metrics

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union["CategoricalMetricInfo", "SystemMetricInfo"]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union["CategoricalMetricInfo", "SystemMetricInfo"]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
