import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
    from ..models.log_records_collection_filter import LogRecordsCollectionFilter
    from ..models.log_records_date_filter import LogRecordsDateFilter
    from ..models.log_records_id_filter import LogRecordsIDFilter
    from ..models.log_records_number_filter import LogRecordsNumberFilter
    from ..models.log_records_text_filter import LogRecordsTextFilter


T = TypeVar("T", bound="LogRecordsMetricsQueryRequest")


@_attrs_define
class LogRecordsMetricsQueryRequest:
    """
    Attributes
    ----------
        start_time (datetime.datetime): Include traces from this time onward.
        end_time (datetime.datetime): Include traces up to this time.
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        metrics_testing_id (Union[None, Unset, str]): Metrics testing id associated with the traces.
        filters (Union[Unset, list[Union['LogRecordsBooleanFilter', 'LogRecordsCollectionFilter',
            'LogRecordsDateFilter', 'LogRecordsIDFilter', 'LogRecordsNumberFilter', 'LogRecordsTextFilter']]]):
        interval (Union[Unset, int]):  Default: 5.
        group_by (Union[None, Unset, str]):
    """

    start_time: datetime.datetime
    end_time: datetime.datetime
    log_stream_id: Union[None, Unset, str] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    metrics_testing_id: Union[None, Unset, str] = UNSET
    filters: Union[
        Unset,
        list[
            Union[
                "LogRecordsBooleanFilter",
                "LogRecordsCollectionFilter",
                "LogRecordsDateFilter",
                "LogRecordsIDFilter",
                "LogRecordsNumberFilter",
                "LogRecordsTextFilter",
            ]
        ],
    ] = UNSET
    interval: Union[Unset, int] = 5
    group_by: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter

        start_time = self.start_time.isoformat()

        end_time = self.end_time.isoformat()

        log_stream_id: Union[None, Unset, str]
        log_stream_id = UNSET if isinstance(self.log_stream_id, Unset) else self.log_stream_id

        experiment_id: Union[None, Unset, str]
        experiment_id = UNSET if isinstance(self.experiment_id, Unset) else self.experiment_id

        metrics_testing_id: Union[None, Unset, str]
        metrics_testing_id = UNSET if isinstance(self.metrics_testing_id, Unset) else self.metrics_testing_id

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(
                    filters_item_data,
                    (
                        LogRecordsIDFilter,
                        LogRecordsDateFilter,
                        LogRecordsNumberFilter,
                        LogRecordsBooleanFilter,
                        LogRecordsCollectionFilter,
                    ),
                ):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        interval = self.interval

        group_by: Union[None, Unset, str]
        group_by = UNSET if isinstance(self.group_by, Unset) else self.group_by

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
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_text_filter import LogRecordsTextFilter

        d = dict(src_dict)
        start_time = isoparse(d.pop("start_time"))

        end_time = isoparse(d.pop("end_time"))

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_experiment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_metrics_testing_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metrics_testing_id = _parse_metrics_testing_id(d.pop("metrics_testing_id", UNSET))

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(
                data: object,
            ) -> Union[
                "LogRecordsBooleanFilter",
                "LogRecordsCollectionFilter",
                "LogRecordsDateFilter",
                "LogRecordsIDFilter",
                "LogRecordsNumberFilter",
                "LogRecordsTextFilter",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsIDFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsDateFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsNumberFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsBooleanFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsCollectionFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                return LogRecordsTextFilter.from_dict(data)

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        interval = d.pop("interval", UNSET)

        def _parse_group_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

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
