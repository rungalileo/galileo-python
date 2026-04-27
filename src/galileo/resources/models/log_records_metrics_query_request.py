from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
    from ..models.log_records_collection_filter import LogRecordsCollectionFilter
    from ..models.log_records_date_filter import LogRecordsDateFilter
    from ..models.log_records_fully_annotated_filter import LogRecordsFullyAnnotatedFilter
    from ..models.log_records_id_filter import LogRecordsIDFilter
    from ..models.log_records_number_filter import LogRecordsNumberFilter
    from ..models.log_records_text_filter import LogRecordsTextFilter


T = TypeVar("T", bound="LogRecordsMetricsQueryRequest")


@_attrs_define
class LogRecordsMetricsQueryRequest:
    """
    Attributes:
        start_time (datetime.datetime): Include traces from this time onward.
        end_time (datetime.datetime): Include traces up to this time.
        log_stream_id (None | str | Unset): Log stream id associated with the traces.
        experiment_id (None | str | Unset): Experiment id associated with the traces.
        metrics_testing_id (None | str | Unset): Metrics testing id associated with the traces.
        filters (list[LogRecordsBooleanFilter | LogRecordsCollectionFilter | LogRecordsDateFilter |
            LogRecordsFullyAnnotatedFilter | LogRecordsIDFilter | LogRecordsNumberFilter | LogRecordsTextFilter] | Unset):
        interval (int | Unset):  Default: 5.
        group_by (None | str | Unset):
    """

    start_time: datetime.datetime
    end_time: datetime.datetime
    log_stream_id: None | str | Unset = UNSET
    experiment_id: None | str | Unset = UNSET
    metrics_testing_id: None | str | Unset = UNSET
    filters: (
        list[
            LogRecordsBooleanFilter
            | LogRecordsCollectionFilter
            | LogRecordsDateFilter
            | LogRecordsFullyAnnotatedFilter
            | LogRecordsIDFilter
            | LogRecordsNumberFilter
            | LogRecordsTextFilter
        ]
        | Unset
    ) = UNSET
    interval: int | Unset = 5
    group_by: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_text_filter import LogRecordsTextFilter

        start_time = self.start_time.isoformat()

        end_time = self.end_time.isoformat()

        log_stream_id: None | str | Unset
        if isinstance(self.log_stream_id, Unset):
            log_stream_id = UNSET
        else:
            log_stream_id = self.log_stream_id

        experiment_id: None | str | Unset
        if isinstance(self.experiment_id, Unset):
            experiment_id = UNSET
        else:
            experiment_id = self.experiment_id

        metrics_testing_id: None | str | Unset
        if isinstance(self.metrics_testing_id, Unset):
            metrics_testing_id = UNSET
        else:
            metrics_testing_id = self.metrics_testing_id

        filters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(filters_item_data, LogRecordsIDFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, LogRecordsDateFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, LogRecordsNumberFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, LogRecordsBooleanFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, LogRecordsCollectionFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, LogRecordsTextFilter):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        interval = self.interval

        group_by: None | str | Unset
        if isinstance(self.group_by, Unset):
            group_by = UNSET
        else:
            group_by = self.group_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"start_time": start_time, "end_time": end_time})
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if metrics_testing_id is not UNSET:
            field_dict["metrics_testing_id"] = metrics_testing_id
        if filters is not UNSET:
            field_dict["filters"] = filters
        if interval is not UNSET:
            field_dict["interval"] = interval
        if group_by is not UNSET:
            field_dict["group_by"] = group_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_fully_annotated_filter import LogRecordsFullyAnnotatedFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_text_filter import LogRecordsTextFilter

        d = dict(src_dict)
        start_time = isoparse(d.pop("start_time"))

        end_time = isoparse(d.pop("end_time"))

        def _parse_log_stream_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_experiment_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_metrics_testing_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metrics_testing_id = _parse_metrics_testing_id(d.pop("metrics_testing_id", UNSET))

        _filters = d.pop("filters", UNSET)
        filters: (
            list[
                LogRecordsBooleanFilter
                | LogRecordsCollectionFilter
                | LogRecordsDateFilter
                | LogRecordsFullyAnnotatedFilter
                | LogRecordsIDFilter
                | LogRecordsNumberFilter
                | LogRecordsTextFilter
            ]
            | Unset
        ) = UNSET
        if _filters is not UNSET:
            filters = []
            for filters_item_data in _filters:

                def _parse_filters_item(
                    data: object,
                ) -> (
                    LogRecordsBooleanFilter
                    | LogRecordsCollectionFilter
                    | LogRecordsDateFilter
                    | LogRecordsFullyAnnotatedFilter
                    | LogRecordsIDFilter
                    | LogRecordsNumberFilter
                    | LogRecordsTextFilter
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_item_type_0 = LogRecordsIDFilter.from_dict(data)

                        return filters_item_type_0
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_item_type_1 = LogRecordsDateFilter.from_dict(data)

                        return filters_item_type_1
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_item_type_2 = LogRecordsNumberFilter.from_dict(data)

                        return filters_item_type_2
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_item_type_3 = LogRecordsBooleanFilter.from_dict(data)

                        return filters_item_type_3
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_item_type_4 = LogRecordsCollectionFilter.from_dict(data)

                        return filters_item_type_4
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_item_type_5 = LogRecordsTextFilter.from_dict(data)

                        return filters_item_type_5
                    except:  # noqa: E722
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_6 = LogRecordsFullyAnnotatedFilter.from_dict(data)

                    return filters_item_type_6

                filters_item = _parse_filters_item(filters_item_data)

                filters.append(filters_item)

        interval = d.pop("interval", UNSET)

        def _parse_group_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group_by = _parse_group_by(d.pop("group_by", UNSET))

        log_records_metrics_query_request = cls(
            start_time=start_time,
            end_time=end_time,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            filters=filters,
            interval=interval,
            group_by=group_by,
        )

        log_records_metrics_query_request.additional_properties = d
        return log_records_metrics_query_request

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
