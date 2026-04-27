from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_records_metrics_response_aggregate_metrics import LogRecordsMetricsResponseAggregateMetrics
    from ..models.log_records_metrics_response_bucketed_metrics import LogRecordsMetricsResponseBucketedMetrics
    from ..models.log_records_metrics_response_standard_errors_type_0 import (
        LogRecordsMetricsResponseStandardErrorsType0,
    )


T = TypeVar("T", bound="LogRecordsMetricsResponse")


@_attrs_define
class LogRecordsMetricsResponse:
    """
    Attributes:
        group_by_columns (list[str]):
        aggregate_metrics (LogRecordsMetricsResponseAggregateMetrics):
        bucketed_metrics (LogRecordsMetricsResponseBucketedMetrics):
        ems_captured_error (bool | Unset): Whether any EMS error codes were encountered in the queried metrics Default:
            False.
        standard_errors (LogRecordsMetricsResponseStandardErrorsType0 | None | Unset): Structured EMS errors for each
            error code encountered, keyed by code
    """

    group_by_columns: list[str]
    aggregate_metrics: LogRecordsMetricsResponseAggregateMetrics
    bucketed_metrics: LogRecordsMetricsResponseBucketedMetrics
    ems_captured_error: bool | Unset = False
    standard_errors: LogRecordsMetricsResponseStandardErrorsType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_records_metrics_response_standard_errors_type_0 import (
            LogRecordsMetricsResponseStandardErrorsType0,
        )

        group_by_columns = self.group_by_columns

        aggregate_metrics = self.aggregate_metrics.to_dict()

        bucketed_metrics = self.bucketed_metrics.to_dict()

        ems_captured_error = self.ems_captured_error

        standard_errors: dict[str, Any] | None | Unset
        if isinstance(self.standard_errors, Unset):
            standard_errors = UNSET
        elif isinstance(self.standard_errors, LogRecordsMetricsResponseStandardErrorsType0):
            standard_errors = self.standard_errors.to_dict()
        else:
            standard_errors = self.standard_errors

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group_by_columns": group_by_columns,
                "aggregate_metrics": aggregate_metrics,
                "bucketed_metrics": bucketed_metrics,
            }
        )
        if ems_captured_error is not UNSET:
            field_dict["ems_captured_error"] = ems_captured_error
        if standard_errors is not UNSET:
            field_dict["standard_errors"] = standard_errors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_records_metrics_response_aggregate_metrics import LogRecordsMetricsResponseAggregateMetrics
        from ..models.log_records_metrics_response_bucketed_metrics import LogRecordsMetricsResponseBucketedMetrics
        from ..models.log_records_metrics_response_standard_errors_type_0 import (
            LogRecordsMetricsResponseStandardErrorsType0,
        )

        d = dict(src_dict)
        group_by_columns = cast(list[str], d.pop("group_by_columns"))

        aggregate_metrics = LogRecordsMetricsResponseAggregateMetrics.from_dict(d.pop("aggregate_metrics"))

        bucketed_metrics = LogRecordsMetricsResponseBucketedMetrics.from_dict(d.pop("bucketed_metrics"))

        ems_captured_error = d.pop("ems_captured_error", UNSET)

        def _parse_standard_errors(data: object) -> LogRecordsMetricsResponseStandardErrorsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                standard_errors_type_0 = LogRecordsMetricsResponseStandardErrorsType0.from_dict(data)

                return standard_errors_type_0
            except:  # noqa: E722
                pass
            return cast(LogRecordsMetricsResponseStandardErrorsType0 | None | Unset, data)

        standard_errors = _parse_standard_errors(d.pop("standard_errors", UNSET))

        log_records_metrics_response = cls(
            group_by_columns=group_by_columns,
            aggregate_metrics=aggregate_metrics,
            bucketed_metrics=bucketed_metrics,
            ems_captured_error=ems_captured_error,
            standard_errors=standard_errors,
        )

        log_records_metrics_response.additional_properties = d
        return log_records_metrics_response

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
