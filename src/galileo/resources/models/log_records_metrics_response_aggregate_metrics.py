from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.log_records_metrics_response_aggregate_metrics_additional_property_type_2 import (
        LogRecordsMetricsResponseAggregateMetricsAdditionalPropertyType2,
    )


T = TypeVar("T", bound="LogRecordsMetricsResponseAggregateMetrics")


@_attrs_define
class LogRecordsMetricsResponseAggregateMetrics:
    """ """

    additional_properties: dict[
        str, Union["LogRecordsMetricsResponseAggregateMetricsAdditionalPropertyType2", float, int]
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_records_metrics_response_aggregate_metrics_additional_property_type_2 import (
            LogRecordsMetricsResponseAggregateMetricsAdditionalPropertyType2,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, LogRecordsMetricsResponseAggregateMetricsAdditionalPropertyType2):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_records_metrics_response_aggregate_metrics_additional_property_type_2 import (
            LogRecordsMetricsResponseAggregateMetricsAdditionalPropertyType2,
        )

        d = dict(src_dict)
        log_records_metrics_response_aggregate_metrics = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union["LogRecordsMetricsResponseAggregateMetricsAdditionalPropertyType2", float, int]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsMetricsResponseAggregateMetricsAdditionalPropertyType2.from_dict(data)

                except:  # noqa: E722
                    pass
                return cast(Union["LogRecordsMetricsResponseAggregateMetricsAdditionalPropertyType2", float, int], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        log_records_metrics_response_aggregate_metrics.additional_properties = additional_properties
        return log_records_metrics_response_aggregate_metrics

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> Union["LogRecordsMetricsResponseAggregateMetricsAdditionalPropertyType2", float, int]:
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: Union["LogRecordsMetricsResponseAggregateMetricsAdditionalPropertyType2", float, int]
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
