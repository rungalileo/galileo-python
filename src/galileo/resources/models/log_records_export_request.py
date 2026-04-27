from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.llm_export_format import LLMExportFormat
from ..models.root_type import RootType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
    from ..models.log_records_collection_filter import LogRecordsCollectionFilter
    from ..models.log_records_date_filter import LogRecordsDateFilter
    from ..models.log_records_fully_annotated_filter import LogRecordsFullyAnnotatedFilter
    from ..models.log_records_id_filter import LogRecordsIDFilter
    from ..models.log_records_number_filter import LogRecordsNumberFilter
    from ..models.log_records_sort_clause import LogRecordsSortClause
    from ..models.log_records_text_filter import LogRecordsTextFilter


T = TypeVar("T", bound="LogRecordsExportRequest")


@_attrs_define
class LogRecordsExportRequest:
    """Request schema for exporting log records (sessions, traces, spans).

    Attributes:
        root_type (RootType): The root-level type of a logged step hierarchy.

            Maps fine-grained StepType values to the three top-level categories
            used throughout the platform: session, trace, and span.
        log_stream_id (None | str | Unset): Log stream id associated with the traces.
        experiment_id (None | str | Unset): Experiment id associated with the traces.
        metrics_testing_id (None | str | Unset): Metrics testing id associated with the traces.
        filters (list[LogRecordsBooleanFilter | LogRecordsCollectionFilter | LogRecordsDateFilter |
            LogRecordsFullyAnnotatedFilter | LogRecordsIDFilter | LogRecordsNumberFilter | LogRecordsTextFilter] | Unset):
            Filters to apply on the export
        sort (LogRecordsSortClause | None | Unset): Sort clause for the export.  Defaults to native sort (created_at, id
            descending).
        column_ids (list[str] | None | Unset): Column IDs to include in export
        export_format (LLMExportFormat | Unset):
        redact (bool | Unset): Redact sensitive data Default: True.
        file_name (None | str | Unset): Optional filename for the exported file
    """

    root_type: RootType
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
    sort: LogRecordsSortClause | None | Unset = UNSET
    column_ids: list[str] | None | Unset = UNSET
    export_format: LLMExportFormat | Unset = UNSET
    redact: bool | Unset = True
    file_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_sort_clause import LogRecordsSortClause
        from ..models.log_records_text_filter import LogRecordsTextFilter

        root_type = self.root_type.value

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

        sort: dict[str, Any] | None | Unset
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, LogRecordsSortClause):
            sort = self.sort.to_dict()
        else:
            sort = self.sort

        column_ids: list[str] | None | Unset
        if isinstance(self.column_ids, Unset):
            column_ids = UNSET
        elif isinstance(self.column_ids, list):
            column_ids = self.column_ids

        else:
            column_ids = self.column_ids

        export_format: str | Unset = UNSET
        if not isinstance(self.export_format, Unset):
            export_format = self.export_format.value

        redact = self.redact

        file_name: None | str | Unset
        if isinstance(self.file_name, Unset):
            file_name = UNSET
        else:
            file_name = self.file_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"root_type": root_type})
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if metrics_testing_id is not UNSET:
            field_dict["metrics_testing_id"] = metrics_testing_id
        if filters is not UNSET:
            field_dict["filters"] = filters
        if sort is not UNSET:
            field_dict["sort"] = sort
        if column_ids is not UNSET:
            field_dict["column_ids"] = column_ids
        if export_format is not UNSET:
            field_dict["export_format"] = export_format
        if redact is not UNSET:
            field_dict["redact"] = redact
        if file_name is not UNSET:
            field_dict["file_name"] = file_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_fully_annotated_filter import LogRecordsFullyAnnotatedFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_sort_clause import LogRecordsSortClause
        from ..models.log_records_text_filter import LogRecordsTextFilter

        d = dict(src_dict)
        root_type = RootType(d.pop("root_type"))

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

        def _parse_column_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                column_ids_type_0 = cast(list[str], data)

                return column_ids_type_0
            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        column_ids = _parse_column_ids(d.pop("column_ids", UNSET))

        _export_format = d.pop("export_format", UNSET)
        export_format: LLMExportFormat | Unset
        if isinstance(_export_format, Unset):
            export_format = UNSET
        else:
            export_format = LLMExportFormat(_export_format)

        redact = d.pop("redact", UNSET)

        def _parse_file_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_name = _parse_file_name(d.pop("file_name", UNSET))

        log_records_export_request = cls(
            root_type=root_type,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            filters=filters,
            sort=sort,
            column_ids=column_ids,
            export_format=export_format,
            redact=redact,
            file_name=file_name,
        )

        log_records_export_request.additional_properties = d
        return log_records_export_request

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
