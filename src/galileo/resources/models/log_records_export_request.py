from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.llm_export_format import LLMExportFormat
from ..models.root_type import RootType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
    from ..models.log_records_date_filter import LogRecordsDateFilter
    from ..models.log_records_id_filter import LogRecordsIDFilter
    from ..models.log_records_number_filter import LogRecordsNumberFilter
    from ..models.log_records_sort_clause import LogRecordsSortClause
    from ..models.log_records_text_filter import LogRecordsTextFilter


T = TypeVar("T", bound="LogRecordsExportRequest")


@_attrs_define
class LogRecordsExportRequest:
    """Request schema for exporting log records (sessions, traces, spans).

    Attributes:
        root_type (RootType):
        column_ids (Union[None, Unset, list[str]]): Column IDs to include in export
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        export_format (Union[Unset, LLMExportFormat]):
        filters (Union[Unset, list[Union['LogRecordsBooleanFilter', 'LogRecordsDateFilter', 'LogRecordsIDFilter',
            'LogRecordsNumberFilter', 'LogRecordsTextFilter']]]): Filters to apply on the export
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        sort (Union[Unset, LogRecordsSortClause]):
    """

    root_type: RootType
    column_ids: Union[None, Unset, list[str]] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    export_format: Union[Unset, LLMExportFormat] = UNSET
    filters: Union[
        Unset,
        list[
            Union[
                "LogRecordsBooleanFilter",
                "LogRecordsDateFilter",
                "LogRecordsIDFilter",
                "LogRecordsNumberFilter",
                "LogRecordsTextFilter",
            ]
        ],
    ] = UNSET
    log_stream_id: Union[None, Unset, str] = UNSET
    sort: Union[Unset, "LogRecordsSortClause"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter

        root_type = self.root_type.value

        column_ids: Union[None, Unset, list[str]]
        if isinstance(self.column_ids, Unset):
            column_ids = UNSET
        elif isinstance(self.column_ids, list):
            column_ids = self.column_ids

        else:
            column_ids = self.column_ids

        experiment_id: Union[None, Unset, str]
        if isinstance(self.experiment_id, Unset):
            experiment_id = UNSET
        else:
            experiment_id = self.experiment_id

        export_format: Union[Unset, str] = UNSET
        if not isinstance(self.export_format, Unset):
            export_format = self.export_format.value

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
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
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        log_stream_id: Union[None, Unset, str]
        if isinstance(self.log_stream_id, Unset):
            log_stream_id = UNSET
        else:
            log_stream_id = self.log_stream_id

        sort: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sort, Unset):
            sort = self.sort.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"root_type": root_type})
        if column_ids is not UNSET:
            field_dict["column_ids"] = column_ids
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if export_format is not UNSET:
            field_dict["export_format"] = export_format
        if filters is not UNSET:
            field_dict["filters"] = filters
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if sort is not UNSET:
            field_dict["sort"] = sort

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_sort_clause import LogRecordsSortClause
        from ..models.log_records_text_filter import LogRecordsTextFilter

        d = dict(src_dict)
        root_type = RootType(d.pop("root_type"))

        def _parse_column_ids(data: object) -> Union[None, Unset, list[str]]:
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
            return cast(Union[None, Unset, list[str]], data)

        column_ids = _parse_column_ids(d.pop("column_ids", UNSET))

        def _parse_experiment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        _export_format = d.pop("export_format", UNSET)
        export_format: Union[Unset, LLMExportFormat]
        if isinstance(_export_format, Unset):
            export_format = UNSET
        else:
            export_format = LLMExportFormat(_export_format)

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(
                data: object,
            ) -> Union[
                "LogRecordsBooleanFilter",
                "LogRecordsDateFilter",
                "LogRecordsIDFilter",
                "LogRecordsNumberFilter",
                "LogRecordsTextFilter",
            ]:
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
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_4 = LogRecordsTextFilter.from_dict(data)

                return filters_item_type_4

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        _sort = d.pop("sort", UNSET)
        sort: Union[Unset, LogRecordsSortClause]
        if isinstance(_sort, Unset):
            sort = UNSET
        else:
            sort = LogRecordsSortClause.from_dict(_sort)

        log_records_export_request = cls(
            root_type=root_type,
            column_ids=column_ids,
            experiment_id=experiment_id,
            export_format=export_format,
            filters=filters,
            log_stream_id=log_stream_id,
            sort=sort,
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
