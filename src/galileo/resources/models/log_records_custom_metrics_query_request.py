import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.and_node_log_records_filter import AndNodeLogRecordsFilter
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.metric_aggregation_detail import MetricAggregationDetail
    from ..models.not_node_log_records_filter import NotNodeLogRecordsFilter
    from ..models.or_node_log_records_filter import OrNodeLogRecordsFilter


T = TypeVar("T", bound="LogRecordsCustomMetricsQueryRequest")


@_attrs_define
class LogRecordsCustomMetricsQueryRequest:
    """
    Attributes
    ----------
        start_time (datetime.datetime): Include traces from this time onward.
        end_time (datetime.datetime): Include traces up to this time.
        metric_details (list['MetricAggregationDetail']): List of metrics to aggregate with their widget IDs and
            aggregation types (max 100)
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        metrics_testing_id (Union[None, Unset, str]): Metrics testing id associated with the traces.
        filter_tree (Union['AndNodeLogRecordsFilter', 'FilterLeafLogRecordsFilter', 'NotNodeLogRecordsFilter',
            'OrNodeLogRecordsFilter', None, Unset]): Filter expression tree for complex filtering
        interval_minutes (Union[Unset, int]): Time interval in minutes for bucketing Default: 5.
        group_by (Union[None, Unset, str]): Column to group by.
    """

    start_time: datetime.datetime
    end_time: datetime.datetime
    metric_details: list["MetricAggregationDetail"]
    log_stream_id: None | Unset | str = UNSET
    experiment_id: None | Unset | str = UNSET
    metrics_testing_id: None | Unset | str = UNSET
    filter_tree: Union[
        "AndNodeLogRecordsFilter",
        "FilterLeafLogRecordsFilter",
        "NotNodeLogRecordsFilter",
        "OrNodeLogRecordsFilter",
        None,
        Unset,
    ] = UNSET
    interval_minutes: Unset | int = 5
    group_by: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node_log_records_filter import AndNodeLogRecordsFilter
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.not_node_log_records_filter import NotNodeLogRecordsFilter
        from ..models.or_node_log_records_filter import OrNodeLogRecordsFilter

        start_time = self.start_time.isoformat()

        end_time = self.end_time.isoformat()

        metric_details = []
        for metric_details_item_data in self.metric_details:
            metric_details_item = metric_details_item_data.to_dict()
            metric_details.append(metric_details_item)

        log_stream_id: None | Unset | str
        log_stream_id = UNSET if isinstance(self.log_stream_id, Unset) else self.log_stream_id

        experiment_id: None | Unset | str
        experiment_id = UNSET if isinstance(self.experiment_id, Unset) else self.experiment_id

        metrics_testing_id: None | Unset | str
        metrics_testing_id = UNSET if isinstance(self.metrics_testing_id, Unset) else self.metrics_testing_id

        filter_tree: None | Unset | dict[str, Any]
        if isinstance(self.filter_tree, Unset):
            filter_tree = UNSET
        elif isinstance(
            self.filter_tree,
            FilterLeafLogRecordsFilter | AndNodeLogRecordsFilter | OrNodeLogRecordsFilter | NotNodeLogRecordsFilter,
        ):
            filter_tree = self.filter_tree.to_dict()
        else:
            filter_tree = self.filter_tree

        interval_minutes = self.interval_minutes

        group_by: None | Unset | str
        group_by = UNSET if isinstance(self.group_by, Unset) else self.group_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"start_time": start_time, "end_time": end_time, "metric_details": metric_details})
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if metrics_testing_id is not UNSET:
            field_dict["metrics_testing_id"] = metrics_testing_id
        if filter_tree is not UNSET:
            field_dict["filter_tree"] = filter_tree
        if interval_minutes is not UNSET:
            field_dict["interval_minutes"] = interval_minutes
        if group_by is not UNSET:
            field_dict["group_by"] = group_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node_log_records_filter import AndNodeLogRecordsFilter
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.metric_aggregation_detail import MetricAggregationDetail
        from ..models.not_node_log_records_filter import NotNodeLogRecordsFilter
        from ..models.or_node_log_records_filter import OrNodeLogRecordsFilter

        d = dict(src_dict)
        start_time = isoparse(d.pop("start_time"))

        end_time = isoparse(d.pop("end_time"))

        metric_details = []
        _metric_details = d.pop("metric_details")
        for metric_details_item_data in _metric_details:
            metric_details_item = MetricAggregationDetail.from_dict(metric_details_item_data)

            metric_details.append(metric_details_item)

        def _parse_log_stream_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_experiment_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_metrics_testing_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        metrics_testing_id = _parse_metrics_testing_id(d.pop("metrics_testing_id", UNSET))

        def _parse_filter_tree(
            data: object,
        ) -> Union[
            "AndNodeLogRecordsFilter",
            "FilterLeafLogRecordsFilter",
            "NotNodeLogRecordsFilter",
            "OrNodeLogRecordsFilter",
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return FilterLeafLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AndNodeLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return OrNodeLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return NotNodeLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "AndNodeLogRecordsFilter",
                    "FilterLeafLogRecordsFilter",
                    "NotNodeLogRecordsFilter",
                    "OrNodeLogRecordsFilter",
                    None,
                    Unset,
                ],
                data,
            )

        filter_tree = _parse_filter_tree(d.pop("filter_tree", UNSET))

        interval_minutes = d.pop("interval_minutes", UNSET)

        def _parse_group_by(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        group_by = _parse_group_by(d.pop("group_by", UNSET))

        log_records_custom_metrics_query_request = cls(
            start_time=start_time,
            end_time=end_time,
            metric_details=metric_details,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            filter_tree=filter_tree,
            interval_minutes=interval_minutes,
            group_by=group_by,
        )

        log_records_custom_metrics_query_request.additional_properties = d
        return log_records_custom_metrics_query_request

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
