from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_data_id_column_filter import LogDataIDColumnFilter
    from ..models.log_data_node_type_filter import LogDataNodeTypeFilter
    from ..models.standard_column_sort import StandardColumnSort


T = TypeVar("T", bound="LogDataQueryRequest")


@_attrs_define
class LogDataQueryRequest:
    """
    Attributes:
        column_ids (Union[None, Unset, list[str]]): column ids to return in each row
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        filters (Union[Unset, list[Union['LogDataIDColumnFilter', 'LogDataNodeTypeFilter']]]):
        limit (Union[Unset, int]):  Default: 100.
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        sort (Union[Unset, list['StandardColumnSort']]):
        starting_token (Union[Unset, int]):  Default: 0.
    """

    column_ids: Union[None, Unset, list[str]] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    filters: Union[Unset, list[Union["LogDataIDColumnFilter", "LogDataNodeTypeFilter"]]] = UNSET
    limit: Union[Unset, int] = 100
    log_stream_id: Union[None, Unset, str] = UNSET
    sort: Union[Unset, list["StandardColumnSort"]] = UNSET
    starting_token: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_data_node_type_filter import LogDataNodeTypeFilter

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

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(filters_item_data, LogDataNodeTypeFilter):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        limit = self.limit

        log_stream_id: Union[None, Unset, str]
        if isinstance(self.log_stream_id, Unset):
            log_stream_id = UNSET
        else:
            log_stream_id = self.log_stream_id

        sort: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sort, Unset):
            sort = []
            for sort_item_data in self.sort:
                sort_item = sort_item_data.to_dict()
                sort.append(sort_item)

        starting_token = self.starting_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if column_ids is not UNSET:
            field_dict["column_ids"] = column_ids
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if filters is not UNSET:
            field_dict["filters"] = filters
        if limit is not UNSET:
            field_dict["limit"] = limit
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if sort is not UNSET:
            field_dict["sort"] = sort
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.log_data_id_column_filter import LogDataIDColumnFilter
        from ..models.log_data_node_type_filter import LogDataNodeTypeFilter
        from ..models.standard_column_sort import StandardColumnSort

        d = src_dict.copy()

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

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(data: object) -> Union["LogDataIDColumnFilter", "LogDataNodeTypeFilter"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = LogDataNodeTypeFilter.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_1 = LogDataIDColumnFilter.from_dict(data)

                return filters_item_type_1

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        limit = d.pop("limit", UNSET)

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        sort = []
        _sort = d.pop("sort", UNSET)
        for sort_item_data in _sort or []:
            sort_item = StandardColumnSort.from_dict(sort_item_data)

            sort.append(sort_item)

        starting_token = d.pop("starting_token", UNSET)

        log_data_query_request = cls(
            column_ids=column_ids,
            experiment_id=experiment_id,
            filters=filters,
            limit=limit,
            log_stream_id=log_stream_id,
            sort=sort,
            starting_token=starting_token,
        )

        log_data_query_request.additional_properties = d
        return log_data_query_request

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
