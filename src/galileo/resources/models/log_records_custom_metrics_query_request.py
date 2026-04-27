from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.metric_aggregation_detail import MetricAggregationDetail
    from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
    from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput


T = TypeVar("T", bound="LogRecordsCustomMetricsQueryRequest")


@_attrs_define
class LogRecordsCustomMetricsQueryRequest:
    """
    Attributes:
        start_time (datetime.datetime): Include traces from this time onward.
        end_time (datetime.datetime): Include traces up to this time.
        metric_details (list[MetricAggregationDetail]): List of metrics to aggregate with their widget IDs and
            aggregation types (max 100)
        log_stream_id (None | str | Unset): Log stream id associated with the traces.
        experiment_id (None | str | Unset): Experiment id associated with the traces.
        metrics_testing_id (None | str | Unset): Metrics testing id associated with the traces.
        filter_tree (AndNodeLogRecordsFilterInput | FilterLeafLogRecordsFilter | None | NotNodeLogRecordsFilterInput |
            OrNodeLogRecordsFilterInput | Unset): Filter expression tree for complex filtering
        interval_minutes (int | Unset): Time interval in minutes for bucketing Default: 5.
        group_by (None | str | Unset): Column to group by
    """

    start_time: datetime.datetime
    end_time: datetime.datetime
    metric_details: list[MetricAggregationDetail]
    log_stream_id: None | str | Unset = UNSET
    experiment_id: None | str | Unset = UNSET
    metrics_testing_id: None | str | Unset = UNSET
    filter_tree: (
        AndNodeLogRecordsFilterInput
        | FilterLeafLogRecordsFilter
        | None
        | NotNodeLogRecordsFilterInput
        | OrNodeLogRecordsFilterInput
        | Unset
    ) = UNSET
    interval_minutes: int | Unset = 5
    group_by: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
        from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput

        start_time = self.start_time.isoformat()

        end_time = self.end_time.isoformat()

        metric_details = []
        for metric_details_item_data in self.metric_details:
            metric_details_item = metric_details_item_data.to_dict()
            metric_details.append(metric_details_item)

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

        filter_tree: dict[str, Any] | None | Unset
        if isinstance(self.filter_tree, Unset):
            filter_tree = UNSET
        elif isinstance(self.filter_tree, FilterLeafLogRecordsFilter):
            filter_tree = self.filter_tree.to_dict()
        elif isinstance(self.filter_tree, AndNodeLogRecordsFilterInput):
            filter_tree = self.filter_tree.to_dict()
        elif isinstance(self.filter_tree, OrNodeLogRecordsFilterInput):
            filter_tree = self.filter_tree.to_dict()
        elif isinstance(self.filter_tree, NotNodeLogRecordsFilterInput):
            filter_tree = self.filter_tree.to_dict()
        else:
            filter_tree = self.filter_tree

        interval_minutes = self.interval_minutes

        group_by: None | str | Unset
        if isinstance(self.group_by, Unset):
            group_by = UNSET
        else:
            group_by = self.group_by

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
        from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.metric_aggregation_detail import MetricAggregationDetail
        from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
        from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput

        d = dict(src_dict)
        start_time = isoparse(d.pop("start_time"))

        end_time = isoparse(d.pop("end_time"))

        metric_details = []
        _metric_details = d.pop("metric_details")
        for metric_details_item_data in _metric_details:
            metric_details_item = MetricAggregationDetail.from_dict(metric_details_item_data)

            metric_details.append(metric_details_item)

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

        def _parse_filter_tree(
            data: object,
        ) -> (
            AndNodeLogRecordsFilterInput
            | FilterLeafLogRecordsFilter
            | None
            | NotNodeLogRecordsFilterInput
            | OrNodeLogRecordsFilterInput
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_0 = FilterLeafLogRecordsFilter.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_1 = AndNodeLogRecordsFilterInput.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_2 = OrNodeLogRecordsFilterInput.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_3 = NotNodeLogRecordsFilterInput.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_3
            except:  # noqa: E722
                pass
            return cast(
                AndNodeLogRecordsFilterInput
                | FilterLeafLogRecordsFilter
                | None
                | NotNodeLogRecordsFilterInput
                | OrNodeLogRecordsFilterInput
                | Unset,
                data,
            )

        filter_tree = _parse_filter_tree(d.pop("filter_tree", UNSET))

        interval_minutes = d.pop("interval_minutes", UNSET)

        def _parse_group_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

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
