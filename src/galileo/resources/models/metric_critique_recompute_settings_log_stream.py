from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
    from ..models.log_records_collection_filter import LogRecordsCollectionFilter
    from ..models.log_records_date_filter import LogRecordsDateFilter
    from ..models.log_records_fully_annotated_filter import LogRecordsFullyAnnotatedFilter
    from ..models.log_records_id_filter import LogRecordsIDFilter
    from ..models.log_records_number_filter import LogRecordsNumberFilter
    from ..models.log_records_text_filter import LogRecordsTextFilter


T = TypeVar("T", bound="MetricCritiqueRecomputeSettingsLogStream")


@_attrs_define
class MetricCritiqueRecomputeSettingsLogStream:
    """
    Attributes:
        run_id (str):
        mode (Literal['log_stream_filters'] | Unset):  Default: 'log_stream_filters'.
        filters (list[LogRecordsBooleanFilter | LogRecordsCollectionFilter | LogRecordsDateFilter |
            LogRecordsFullyAnnotatedFilter | LogRecordsIDFilter | LogRecordsNumberFilter | LogRecordsTextFilter] | Unset):
            The parsed filters that are used to recompute the metric critique.
    """

    run_id: str
    mode: Literal["log_stream_filters"] | Unset = "log_stream_filters"
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
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_text_filter import LogRecordsTextFilter

        run_id = self.run_id

        mode = self.mode

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"run_id": run_id})
        if mode is not UNSET:
            field_dict["mode"] = mode
        if filters is not UNSET:
            field_dict["filters"] = filters

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
        run_id = d.pop("run_id")

        mode = cast(Literal["log_stream_filters"] | Unset, d.pop("mode", UNSET))
        if mode != "log_stream_filters" and not isinstance(mode, Unset):
            raise ValueError(f"mode must match const 'log_stream_filters', got '{mode}'")

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

        metric_critique_recompute_settings_log_stream = cls(run_id=run_id, mode=mode, filters=filters)

        metric_critique_recompute_settings_log_stream.additional_properties = d
        return metric_critique_recompute_settings_log_stream

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
