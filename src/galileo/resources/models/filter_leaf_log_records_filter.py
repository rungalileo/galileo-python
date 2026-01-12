from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
    from ..models.log_records_collection_filter import LogRecordsCollectionFilter
    from ..models.log_records_date_filter import LogRecordsDateFilter
    from ..models.log_records_id_filter import LogRecordsIDFilter
    from ..models.log_records_number_filter import LogRecordsNumberFilter
    from ..models.log_records_text_filter import LogRecordsTextFilter


T = TypeVar("T", bound="FilterLeafLogRecordsFilter")


@_attrs_define
class FilterLeafLogRecordsFilter:
    """
    Attributes
    ----------
        filter_ (Union['LogRecordsBooleanFilter', 'LogRecordsCollectionFilter', 'LogRecordsDateFilter',
            'LogRecordsIDFilter', 'LogRecordsNumberFilter', 'LogRecordsTextFilter']):
    """

    filter_: Union[
        "LogRecordsBooleanFilter",
        "LogRecordsCollectionFilter",
        "LogRecordsDateFilter",
        "LogRecordsIDFilter",
        "LogRecordsNumberFilter",
        "LogRecordsTextFilter",
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter

        filter_: dict[str, Any]
        if isinstance(
            self.filter_,
            (
                LogRecordsIDFilter,
                LogRecordsDateFilter,
                LogRecordsNumberFilter,
                LogRecordsBooleanFilter,
                LogRecordsCollectionFilter,
            ),
        ):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"filter": filter_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_text_filter import LogRecordsTextFilter

        d = dict(src_dict)

        def _parse_filter_(
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

        filter_ = _parse_filter_(d.pop("filter"))

        filter_leaf_log_records_filter = cls(filter_=filter_)

        filter_leaf_log_records_filter.additional_properties = d
        return filter_leaf_log_records_filter

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
