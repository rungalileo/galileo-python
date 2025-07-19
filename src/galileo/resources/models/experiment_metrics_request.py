from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
    from ..models.log_records_date_filter import LogRecordsDateFilter
    from ..models.log_records_id_filter import LogRecordsIDFilter
    from ..models.log_records_number_filter import LogRecordsNumberFilter
    from ..models.log_records_text_filter import LogRecordsTextFilter


T = TypeVar("T", bound="ExperimentMetricsRequest")


@_attrs_define
class ExperimentMetricsRequest:
    """
    Attributes:
        filters (Union[Unset, list[Union['LogRecordsBooleanFilter', 'LogRecordsDateFilter', 'LogRecordsIDFilter',
            'LogRecordsNumberFilter', 'LogRecordsTextFilter']]]):
    """

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
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_text_filter import LogRecordsTextFilter

        d = dict(src_dict)
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

        experiment_metrics_request = cls(filters=filters)

        experiment_metrics_request.additional_properties = d
        return experiment_metrics_request

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
