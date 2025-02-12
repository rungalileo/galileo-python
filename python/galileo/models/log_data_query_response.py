from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_computing import MetricComputing
    from ..models.metric_error import MetricError
    from ..models.metric_failed import MetricFailed
    from ..models.metric_not_applicable import MetricNotApplicable
    from ..models.metric_not_computed import MetricNotComputed
    from ..models.metric_pending import MetricPending
    from ..models.metric_success import MetricSuccess


T = TypeVar("T", bound="LogDataQueryResponse")


@_attrs_define
class LogDataQueryResponse:
    """
    Attributes:
        column_ids (Union[Unset, list[str]]): column ids present in each row
        limit (Union[Unset, int]):  Default: 100.
        next_starting_token (Union[None, Unset, int]):
        num_rows (Union[Unset, int]): number of data rows
        paginated (Union[Unset, bool]):  Default: False.
        rows (Union[Unset, list[list[Union['MetricComputing', 'MetricError', 'MetricFailed', 'MetricNotApplicable',
            'MetricNotComputed', 'MetricPending', 'MetricSuccess']]]]): list of data rows
        starting_token (Union[Unset, int]):  Default: 0.
    """

    column_ids: Union[Unset, list[str]] = UNSET
    limit: Union[Unset, int] = 100
    next_starting_token: Union[None, Unset, int] = UNSET
    num_rows: Union[Unset, int] = UNSET
    paginated: Union[Unset, bool] = False
    rows: Union[
        Unset,
        list[
            list[
                Union[
                    "MetricComputing",
                    "MetricError",
                    "MetricFailed",
                    "MetricNotApplicable",
                    "MetricNotComputed",
                    "MetricPending",
                    "MetricSuccess",
                ]
            ]
        ],
    ] = UNSET
    starting_token: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_computing import MetricComputing
        from ..models.metric_error import MetricError
        from ..models.metric_not_applicable import MetricNotApplicable
        from ..models.metric_not_computed import MetricNotComputed
        from ..models.metric_pending import MetricPending
        from ..models.metric_success import MetricSuccess

        column_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.column_ids, Unset):
            column_ids = self.column_ids

        limit = self.limit

        next_starting_token: Union[None, Unset, int]
        if isinstance(self.next_starting_token, Unset):
            next_starting_token = UNSET
        else:
            next_starting_token = self.next_starting_token

        num_rows = self.num_rows

        paginated = self.paginated

        rows: Union[Unset, list[list[dict[str, Any]]]] = UNSET
        if not isinstance(self.rows, Unset):
            rows = []
            for rows_item_data in self.rows:
                rows_item = []
                for rows_item_item_data in rows_item_data:
                    rows_item_item: dict[str, Any]
                    if isinstance(rows_item_item_data, MetricNotComputed):
                        rows_item_item = rows_item_item_data.to_dict()
                    elif isinstance(rows_item_item_data, MetricPending):
                        rows_item_item = rows_item_item_data.to_dict()
                    elif isinstance(rows_item_item_data, MetricComputing):
                        rows_item_item = rows_item_item_data.to_dict()
                    elif isinstance(rows_item_item_data, MetricNotApplicable):
                        rows_item_item = rows_item_item_data.to_dict()
                    elif isinstance(rows_item_item_data, MetricSuccess):
                        rows_item_item = rows_item_item_data.to_dict()
                    elif isinstance(rows_item_item_data, MetricError):
                        rows_item_item = rows_item_item_data.to_dict()
                    else:
                        rows_item_item = rows_item_item_data.to_dict()

                    rows_item.append(rows_item_item)

                rows.append(rows_item)

        starting_token = self.starting_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if column_ids is not UNSET:
            field_dict["column_ids"] = column_ids
        if limit is not UNSET:
            field_dict["limit"] = limit
        if next_starting_token is not UNSET:
            field_dict["next_starting_token"] = next_starting_token
        if num_rows is not UNSET:
            field_dict["num_rows"] = num_rows
        if paginated is not UNSET:
            field_dict["paginated"] = paginated
        if rows is not UNSET:
            field_dict["rows"] = rows
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric_computing import MetricComputing
        from ..models.metric_error import MetricError
        from ..models.metric_failed import MetricFailed
        from ..models.metric_not_applicable import MetricNotApplicable
        from ..models.metric_not_computed import MetricNotComputed
        from ..models.metric_pending import MetricPending
        from ..models.metric_success import MetricSuccess

        d = src_dict.copy()
        column_ids = cast(list[str], d.pop("column_ids", UNSET))

        limit = d.pop("limit", UNSET)

        def _parse_next_starting_token(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        next_starting_token = _parse_next_starting_token(d.pop("next_starting_token", UNSET))

        num_rows = d.pop("num_rows", UNSET)

        paginated = d.pop("paginated", UNSET)

        rows = []
        _rows = d.pop("rows", UNSET)
        for rows_item_data in _rows or []:
            rows_item = []
            _rows_item = rows_item_data
            for rows_item_item_data in _rows_item:

                def _parse_rows_item_item(
                    data: object,
                ) -> Union[
                    "MetricComputing",
                    "MetricError",
                    "MetricFailed",
                    "MetricNotApplicable",
                    "MetricNotComputed",
                    "MetricPending",
                    "MetricSuccess",
                ]:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        rows_item_item_type_0 = MetricNotComputed.from_dict(data)

                        return rows_item_item_type_0
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        rows_item_item_type_1 = MetricPending.from_dict(data)

                        return rows_item_item_type_1
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        rows_item_item_type_2 = MetricComputing.from_dict(data)

                        return rows_item_item_type_2
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        rows_item_item_type_3 = MetricNotApplicable.from_dict(data)

                        return rows_item_item_type_3
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        rows_item_item_type_4 = MetricSuccess.from_dict(data)

                        return rows_item_item_type_4
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        rows_item_item_type_5 = MetricError.from_dict(data)

                        return rows_item_item_type_5
                    except:  # noqa: E722
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    rows_item_item_type_6 = MetricFailed.from_dict(data)

                    return rows_item_item_type_6

                rows_item_item = _parse_rows_item_item(rows_item_item_data)

                rows_item.append(rows_item_item)

            rows.append(rows_item)

        starting_token = d.pop("starting_token", UNSET)

        log_data_query_response = cls(
            column_ids=column_ids,
            limit=limit,
            next_starting_token=next_starting_token,
            num_rows=num_rows,
            paginated=paginated,
            rows=rows,
            starting_token=starting_token,
        )

        log_data_query_response.additional_properties = d
        return log_data_query_response

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
