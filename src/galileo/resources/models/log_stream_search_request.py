from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_stream_created_at_filter import LogStreamCreatedAtFilter
    from ..models.log_stream_created_at_sort import LogStreamCreatedAtSort
    from ..models.log_stream_created_by_filter import LogStreamCreatedByFilter
    from ..models.log_stream_id_filter import LogStreamIDFilter
    from ..models.log_stream_name_filter import LogStreamNameFilter
    from ..models.log_stream_name_sort import LogStreamNameSort
    from ..models.log_stream_updated_at_filter import LogStreamUpdatedAtFilter
    from ..models.log_stream_updated_at_sort import LogStreamUpdatedAtSort


T = TypeVar("T", bound="LogStreamSearchRequest")


@_attrs_define
class LogStreamSearchRequest:
    """
    Attributes:
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        filters (Union[Unset, list[Union['LogStreamCreatedAtFilter', 'LogStreamCreatedByFilter', 'LogStreamIDFilter',
            'LogStreamNameFilter', 'LogStreamUpdatedAtFilter']]]):
        sort (Union['LogStreamCreatedAtSort', 'LogStreamNameSort', 'LogStreamUpdatedAtSort', None, Unset]):  Default:
            None.
        include_counts (Union[Unset, bool]):  Default: False.
    """

    starting_token: Union[Unset, int] = 0
    limit: Union[Unset, int] = 100
    filters: Union[
        Unset,
        list[
            Union[
                "LogStreamCreatedAtFilter",
                "LogStreamCreatedByFilter",
                "LogStreamIDFilter",
                "LogStreamNameFilter",
                "LogStreamUpdatedAtFilter",
            ]
        ],
    ] = UNSET
    sort: Union["LogStreamCreatedAtSort", "LogStreamNameSort", "LogStreamUpdatedAtSort", None, Unset] = None
    include_counts: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_stream_created_at_filter import LogStreamCreatedAtFilter
        from ..models.log_stream_created_at_sort import LogStreamCreatedAtSort
        from ..models.log_stream_created_by_filter import LogStreamCreatedByFilter
        from ..models.log_stream_id_filter import LogStreamIDFilter
        from ..models.log_stream_name_filter import LogStreamNameFilter
        from ..models.log_stream_name_sort import LogStreamNameSort
        from ..models.log_stream_updated_at_sort import LogStreamUpdatedAtSort

        starting_token = self.starting_token

        limit = self.limit

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(filters_item_data, LogStreamIDFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, LogStreamNameFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, LogStreamCreatedByFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, LogStreamCreatedAtFilter):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, LogStreamNameSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, LogStreamCreatedAtSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, LogStreamUpdatedAtSort):
            sort = self.sort.to_dict()
        else:
            sort = self.sort

        include_counts = self.include_counts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if limit is not UNSET:
            field_dict["limit"] = limit
        if filters is not UNSET:
            field_dict["filters"] = filters
        if sort is not UNSET:
            field_dict["sort"] = sort
        if include_counts is not UNSET:
            field_dict["include_counts"] = include_counts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_stream_created_at_filter import LogStreamCreatedAtFilter
        from ..models.log_stream_created_at_sort import LogStreamCreatedAtSort
        from ..models.log_stream_created_by_filter import LogStreamCreatedByFilter
        from ..models.log_stream_id_filter import LogStreamIDFilter
        from ..models.log_stream_name_filter import LogStreamNameFilter
        from ..models.log_stream_name_sort import LogStreamNameSort
        from ..models.log_stream_updated_at_filter import LogStreamUpdatedAtFilter
        from ..models.log_stream_updated_at_sort import LogStreamUpdatedAtSort

        d = dict(src_dict)
        starting_token = d.pop("starting_token", UNSET)

        limit = d.pop("limit", UNSET)

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(
                data: object,
            ) -> Union[
                "LogStreamCreatedAtFilter",
                "LogStreamCreatedByFilter",
                "LogStreamIDFilter",
                "LogStreamNameFilter",
                "LogStreamUpdatedAtFilter",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = LogStreamIDFilter.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_1 = LogStreamNameFilter.from_dict(data)

                    return filters_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_2 = LogStreamCreatedByFilter.from_dict(data)

                    return filters_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_3 = LogStreamCreatedAtFilter.from_dict(data)

                    return filters_item_type_3
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_4 = LogStreamUpdatedAtFilter.from_dict(data)

                return filters_item_type_4

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        def _parse_sort(
            data: object,
        ) -> Union["LogStreamCreatedAtSort", "LogStreamNameSort", "LogStreamUpdatedAtSort", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_0 = LogStreamNameSort.from_dict(data)

                return sort_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_1 = LogStreamCreatedAtSort.from_dict(data)

                return sort_type_0_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_2 = LogStreamUpdatedAtSort.from_dict(data)

                return sort_type_0_type_2
            except:  # noqa: E722
                pass
            return cast(
                Union["LogStreamCreatedAtSort", "LogStreamNameSort", "LogStreamUpdatedAtSort", None, Unset], data
            )

        sort = _parse_sort(d.pop("sort", UNSET))

        include_counts = d.pop("include_counts", UNSET)

        log_stream_search_request = cls(
            starting_token=starting_token, limit=limit, filters=filters, sort=sort, include_counts=include_counts
        )

        log_stream_search_request.additional_properties = d
        return log_stream_search_request

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
