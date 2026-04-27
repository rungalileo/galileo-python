from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
    from ..models.log_records_collection_filter import LogRecordsCollectionFilter
    from ..models.log_records_date_filter import LogRecordsDateFilter
    from ..models.log_records_fully_annotated_filter import LogRecordsFullyAnnotatedFilter
    from ..models.log_records_id_filter import LogRecordsIDFilter
    from ..models.log_records_number_filter import LogRecordsNumberFilter
    from ..models.log_records_text_filter import LogRecordsTextFilter
    from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
    from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput


T = TypeVar("T", bound="LogRecordsQueryCountRequest")


@_attrs_define
class LogRecordsQueryCountRequest:
    """
    Example:
        {'filters': [{'case_sensitive': True, 'name': 'input', 'operator': 'eq', 'type': 'text', 'value': 'example
            input'}], 'log_stream_id': '74aec44e-ec21-4c9f-a3e2-b2ab2b81b4db'}

    Attributes:
        log_stream_id (None | str | Unset): Log stream id associated with the traces.
        experiment_id (None | str | Unset): Experiment id associated with the traces.
        metrics_testing_id (None | str | Unset): Metrics testing id associated with the traces.
        filters (list[LogRecordsBooleanFilter | LogRecordsCollectionFilter | LogRecordsDateFilter |
            LogRecordsFullyAnnotatedFilter | LogRecordsIDFilter | LogRecordsNumberFilter | LogRecordsTextFilter] | Unset):
        filter_tree (AndNodeLogRecordsFilterInput | FilterLeafLogRecordsFilter | None | NotNodeLogRecordsFilterInput |
            OrNodeLogRecordsFilterInput | Unset):
    """

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
    filter_tree: (
        AndNodeLogRecordsFilterInput
        | FilterLeafLogRecordsFilter
        | None
        | NotNodeLogRecordsFilterInput
        | OrNodeLogRecordsFilterInput
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_text_filter import LogRecordsTextFilter
        from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
        from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if metrics_testing_id is not UNSET:
            field_dict["metrics_testing_id"] = metrics_testing_id
        if filters is not UNSET:
            field_dict["filters"] = filters
        if filter_tree is not UNSET:
            field_dict["filter_tree"] = filter_tree

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_fully_annotated_filter import LogRecordsFullyAnnotatedFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_text_filter import LogRecordsTextFilter
        from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
        from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput

        d = dict(src_dict)

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

        log_records_query_count_request = cls(
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            filters=filters,
            filter_tree=filter_tree,
        )

        log_records_query_count_request.additional_properties = d
        return log_records_query_count_request

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
