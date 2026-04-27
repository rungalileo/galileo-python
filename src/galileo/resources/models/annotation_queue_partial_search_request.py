from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.log_records_sort_clause import LogRecordsSortClause
    from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
    from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput
    from ..models.select_columns import SelectColumns


T = TypeVar("T", bound="AnnotationQueuePartialSearchRequest")


@_attrs_define
class AnnotationQueuePartialSearchRequest:
    """Request to search records in an annotation queue with partial field selection.

    Similar to LogRecordsPartialQueryRequest but doesn't require log_stream_id/experiment_id
    since the queue determines which project/run pairs to search. This is also
    the queue-scoped search path where the `fully_annotated` filter is supported.

        Attributes:
            select_columns (SelectColumns):
            starting_token (int | Unset):  Default: 0.
            limit (int | Unset):  Default: 100.
            previous_last_row_id (None | str | Unset):
            filter_tree (AndNodeLogRecordsFilterInput | FilterLeafLogRecordsFilter | None | NotNodeLogRecordsFilterInput |
                OrNodeLogRecordsFilterInput | Unset): Filter tree to apply when searching records in the queue. The
                `fully_annotated` filter is only supported on this queue-scoped path.
            sort (LogRecordsSortClause | None | Unset): Sort for the query. Defaults to native sort (created_at, id
                descending).
            truncate_fields (bool | Unset): Whether to truncate long text fields Default: False.
            include_counts (bool | Unset): If True, include computed child counts (e.g., num_traces for sessions, num_spans
                for traces). Default: False.
    """

    select_columns: SelectColumns
    starting_token: int | Unset = 0
    limit: int | Unset = 100
    previous_last_row_id: None | str | Unset = UNSET
    filter_tree: (
        AndNodeLogRecordsFilterInput
        | FilterLeafLogRecordsFilter
        | None
        | NotNodeLogRecordsFilterInput
        | OrNodeLogRecordsFilterInput
        | Unset
    ) = UNSET
    sort: LogRecordsSortClause | None | Unset = UNSET
    truncate_fields: bool | Unset = False
    include_counts: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.log_records_sort_clause import LogRecordsSortClause
        from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
        from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput

        select_columns = self.select_columns.to_dict()

        starting_token = self.starting_token

        limit = self.limit

        previous_last_row_id: None | str | Unset
        if isinstance(self.previous_last_row_id, Unset):
            previous_last_row_id = UNSET
        else:
            previous_last_row_id = self.previous_last_row_id

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

        sort: dict[str, Any] | None | Unset
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, LogRecordsSortClause):
            sort = self.sort.to_dict()
        else:
            sort = self.sort

        truncate_fields = self.truncate_fields

        include_counts = self.include_counts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"select_columns": select_columns})
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if limit is not UNSET:
            field_dict["limit"] = limit
        if previous_last_row_id is not UNSET:
            field_dict["previous_last_row_id"] = previous_last_row_id
        if filter_tree is not UNSET:
            field_dict["filter_tree"] = filter_tree
        if sort is not UNSET:
            field_dict["sort"] = sort
        if truncate_fields is not UNSET:
            field_dict["truncate_fields"] = truncate_fields
        if include_counts is not UNSET:
            field_dict["include_counts"] = include_counts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.log_records_sort_clause import LogRecordsSortClause
        from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
        from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput
        from ..models.select_columns import SelectColumns

        d = dict(src_dict)
        select_columns = SelectColumns.from_dict(d.pop("select_columns"))

        starting_token = d.pop("starting_token", UNSET)

        limit = d.pop("limit", UNSET)

        def _parse_previous_last_row_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        previous_last_row_id = _parse_previous_last_row_id(d.pop("previous_last_row_id", UNSET))

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

        def _parse_sort(data: object) -> LogRecordsSortClause | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0 = LogRecordsSortClause.from_dict(data)

                return sort_type_0
            except:  # noqa: E722
                pass
            return cast(LogRecordsSortClause | None | Unset, data)

        sort = _parse_sort(d.pop("sort", UNSET))

        truncate_fields = d.pop("truncate_fields", UNSET)

        include_counts = d.pop("include_counts", UNSET)

        annotation_queue_partial_search_request = cls(
            select_columns=select_columns,
            starting_token=starting_token,
            limit=limit,
            previous_last_row_id=previous_last_row_id,
            filter_tree=filter_tree,
            sort=sort,
            truncate_fields=truncate_fields,
            include_counts=include_counts,
        )

        annotation_queue_partial_search_request.additional_properties = d
        return annotation_queue_partial_search_request

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
