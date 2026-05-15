from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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

    Attributes
    ----------
        root_type (RootType): The root-level type of a logged step hierarchy.

            Maps fine-grained StepType values to the three top-level categories
            used throughout the platform: session, trace, and span.
        column_ids (Union[None, Unset, list[str]]): Column IDs to include in the export. Applies only to CSV exports.
        export_format (Union[Unset, LLMExportFormat]):
        redact (Union[Unset, bool]): Redact sensitive data Default: True.
        file_name (Union[None, Unset, str]): Optional filename for the exported file
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        metrics_testing_id (Union[None, Unset, str]): Metrics testing id associated with the traces.
        filters (Union[Unset, list[Union['LogRecordsBooleanFilter', 'LogRecordsCollectionFilter',
            'LogRecordsDateFilter', 'LogRecordsFullyAnnotatedFilter', 'LogRecordsIDFilter', 'LogRecordsNumberFilter',
            'LogRecordsTextFilter']]]): Filters to apply on the export
        sort (Union['LogRecordsSortClause', None, Unset]): Sort clause for the export.  Defaults to native sort
            (created_at, id descending).
        include_code_metric_metadata (Union[Unset, bool]): If True, include per-row scorer metadata (the dict
            returned alongside the score by code-based scorers via the (score, metadata) tuple-return contract) on
            each MetricSuccess in the export. Default: False.
    """

    root_type: RootType
    column_ids: None | Unset | list[str] = UNSET
    export_format: Unset | LLMExportFormat = UNSET
    redact: Unset | bool = True
    file_name: None | Unset | str = UNSET
    log_stream_id: None | Unset | str = UNSET
    experiment_id: None | Unset | str = UNSET
    metrics_testing_id: None | Unset | str = UNSET
    filters: (
        Unset
        | list[
            Union[
                "LogRecordsBooleanFilter",
                "LogRecordsCollectionFilter",
                "LogRecordsDateFilter",
                "LogRecordsFullyAnnotatedFilter",
                "LogRecordsIDFilter",
                "LogRecordsNumberFilter",
                "LogRecordsTextFilter",
            ]
        ]
    ) = UNSET
    sort: Union["LogRecordsSortClause", None, Unset] = UNSET
    include_code_metric_metadata: Unset | bool = False
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

        column_ids: None | Unset | list[str]
        if isinstance(self.column_ids, Unset):
            column_ids = UNSET
        elif isinstance(self.column_ids, list):
            column_ids = self.column_ids

        else:
            column_ids = self.column_ids

        export_format: Unset | str = UNSET
        if not isinstance(self.export_format, Unset):
            export_format = self.export_format.value

        redact = self.redact

        file_name: None | Unset | str
        file_name = UNSET if isinstance(self.file_name, Unset) else self.file_name

        log_stream_id: None | Unset | str
        log_stream_id = UNSET if isinstance(self.log_stream_id, Unset) else self.log_stream_id

        experiment_id: None | Unset | str
        experiment_id = UNSET if isinstance(self.experiment_id, Unset) else self.experiment_id

        metrics_testing_id: None | Unset | str
        metrics_testing_id = UNSET if isinstance(self.metrics_testing_id, Unset) else self.metrics_testing_id

        filters: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(
                    filters_item_data,
                    LogRecordsIDFilter
                    | LogRecordsDateFilter
                    | LogRecordsNumberFilter
                    | LogRecordsBooleanFilter
                    | (LogRecordsCollectionFilter | LogRecordsTextFilter),
                ):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sort: None | Unset | dict[str, Any]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, LogRecordsSortClause):
            sort = self.sort.to_dict()
        else:
            sort = self.sort

        include_code_metric_metadata = self.include_code_metric_metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"root_type": root_type})
        if column_ids is not UNSET:
            field_dict["column_ids"] = column_ids
        if export_format is not UNSET:
            field_dict["export_format"] = export_format
        if redact is not UNSET:
            field_dict["redact"] = redact
        if file_name is not UNSET:
            field_dict["file_name"] = file_name
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
        if include_code_metric_metadata is not UNSET:
            field_dict["include_code_metric_metadata"] = include_code_metric_metadata

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

        def _parse_column_ids(data: object) -> None | Unset | list[str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(None | Unset | list[str], data)

        column_ids = _parse_column_ids(d.pop("column_ids", UNSET))

        _export_format = d.pop("export_format", UNSET)
        export_format: Unset | LLMExportFormat
        export_format = UNSET if isinstance(_export_format, Unset) else LLMExportFormat(_export_format)

        redact = d.pop("redact", UNSET)

        def _parse_file_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        file_name = _parse_file_name(d.pop("file_name", UNSET))

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

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(
                data: object,
            ) -> Union[
                "LogRecordsBooleanFilter",
                "LogRecordsCollectionFilter",
                "LogRecordsDateFilter",
                "LogRecordsFullyAnnotatedFilter",
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
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsTextFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                return LogRecordsFullyAnnotatedFilter.from_dict(data)

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        def _parse_sort(data: object) -> Union["LogRecordsSortClause", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return LogRecordsSortClause.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["LogRecordsSortClause", None, Unset], data)

        sort = _parse_sort(d.pop("sort", UNSET))

        include_code_metric_metadata = d.pop("include_code_metric_metadata", UNSET)

        log_records_export_request = cls(
            root_type=root_type,
            column_ids=column_ids,
            export_format=export_format,
            redact=redact,
            file_name=file_name,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            filters=filters,
            sort=sort,
            include_code_metric_metadata=include_code_metric_metadata,
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
