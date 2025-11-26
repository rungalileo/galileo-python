from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.and_node import AndNode
    from ..models.filter_leaf import FilterLeaf
    from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
    from ..models.log_records_collection_filter import LogRecordsCollectionFilter
    from ..models.log_records_date_filter import LogRecordsDateFilter
    from ..models.log_records_id_filter import LogRecordsIDFilter
    from ..models.log_records_number_filter import LogRecordsNumberFilter
    from ..models.log_records_sort_clause import LogRecordsSortClause
    from ..models.log_records_text_filter import LogRecordsTextFilter
    from ..models.not_node import NotNode
    from ..models.or_node import OrNode


T = TypeVar("T", bound="RecomputeLogRecordsMetricsRequest")


@_attrs_define
class RecomputeLogRecordsMetricsRequest:
    """Request to recompute metrics for a genai project run (log stream or experiment).
    This request is used to trigger recomputation of metrics based on the provided filters and scorer IDs.

    Attributes
    ----------
            scorer_ids (list[str]): List of scorer IDs for which metrics should be recomputed.
            starting_token (Union[Unset, int]):  Default: 0.
            limit (Union[Unset, int]):  Default: 100.
            previous_last_row_id (Union[None, Unset, str]):
            log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
            experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
            metrics_testing_id (Union[None, Unset, str]): Metrics testing id associated with the traces.
            filters (Union[Unset, list[Union['LogRecordsBooleanFilter', 'LogRecordsCollectionFilter',
                'LogRecordsDateFilter', 'LogRecordsIDFilter', 'LogRecordsNumberFilter', 'LogRecordsTextFilter']]]):
            filter_tree (Union['AndNode', 'FilterLeaf', 'NotNode', 'OrNode', None, Unset]):
            sort (Union[Unset, LogRecordsSortClause]):
            truncate_fields (Union[Unset, bool]):  Default: False.
    """

    scorer_ids: list[str]
    starting_token: Union[Unset, int] = 0
    limit: Union[Unset, int] = 100
    previous_last_row_id: Union[None, Unset, str] = UNSET
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
    filter_tree: Union["AndNode", "FilterLeaf", "NotNode", "OrNode", None, Unset] = UNSET
    sort: Union[Unset, "LogRecordsSortClause"] = UNSET
    truncate_fields: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node import AndNode
        from ..models.filter_leaf import FilterLeaf
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.not_node import NotNode
        from ..models.or_node import OrNode

        scorer_ids = self.scorer_ids

        starting_token = self.starting_token

        limit = self.limit

        previous_last_row_id: Union[None, Unset, str]
        previous_last_row_id = UNSET if isinstance(self.previous_last_row_id, Unset) else self.previous_last_row_id

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

        filter_tree: Union[None, Unset, dict[str, Any]]
        if isinstance(self.filter_tree, Unset):
            filter_tree = UNSET
        elif isinstance(self.filter_tree, (FilterLeaf, AndNode, OrNode, NotNode)):
            filter_tree = self.filter_tree.to_dict()
        else:
            filter_tree = self.filter_tree

        sort: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sort, Unset):
            sort = self.sort.to_dict()

        truncate_fields = self.truncate_fields

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"scorer_ids": scorer_ids})
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if limit is not UNSET:
            field_dict["limit"] = limit
        if previous_last_row_id is not UNSET:
            field_dict["previous_last_row_id"] = previous_last_row_id
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
        if sort is not UNSET:
            field_dict["sort"] = sort
        if truncate_fields is not UNSET:
            field_dict["truncate_fields"] = truncate_fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node import AndNode
        from ..models.filter_leaf import FilterLeaf
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_sort_clause import LogRecordsSortClause
        from ..models.log_records_text_filter import LogRecordsTextFilter
        from ..models.not_node import NotNode
        from ..models.or_node import OrNode

        d = dict(src_dict)
        scorer_ids = cast(list[str], d.pop("scorer_ids"))

        starting_token = d.pop("starting_token", UNSET)

        limit = d.pop("limit", UNSET)

        def _parse_previous_last_row_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        previous_last_row_id = _parse_previous_last_row_id(d.pop("previous_last_row_id", UNSET))

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

        def _parse_filter_tree(data: object) -> Union["AndNode", "FilterLeaf", "NotNode", "OrNode", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return FilterLeaf.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AndNode.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return OrNode.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return NotNode.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["AndNode", "FilterLeaf", "NotNode", "OrNode", None, Unset], data)

        filter_tree = _parse_filter_tree(d.pop("filter_tree", UNSET))

        _sort = d.pop("sort", UNSET)
        sort: Union[Unset, LogRecordsSortClause]
        sort = UNSET if isinstance(_sort, Unset) else LogRecordsSortClause.from_dict(_sort)

        truncate_fields = d.pop("truncate_fields", UNSET)

        recompute_log_records_metrics_request = cls(
            scorer_ids=scorer_ids,
            starting_token=starting_token,
            limit=limit,
            previous_last_row_id=previous_last_row_id,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            filters=filters,
            filter_tree=filter_tree,
            sort=sort,
            truncate_fields=truncate_fields,
        )

        recompute_log_records_metrics_request.additional_properties = d
        return recompute_log_records_metrics_request

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
