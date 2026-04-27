from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.query_filter_v1 import QueryFilterV1
    from ..models.sort_clause import SortClause


T = TypeVar("T", bound="TransactionRowsRequestBody")


@_attrs_define
class TransactionRowsRequestBody:
    """
    Attributes:
        filters (list[QueryFilterV1] | Unset):
        sort_spec (list[SortClause] | Unset):
        columns (list[str] | None | Unset):
    """

    filters: list[QueryFilterV1] | Unset = UNSET
    sort_spec: list[SortClause] | Unset = UNSET
    columns: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)

        sort_spec: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sort_spec, Unset):
            sort_spec = []
            for sort_spec_item_data in self.sort_spec:
                sort_spec_item = sort_spec_item_data.to_dict()
                sort_spec.append(sort_spec_item)

        columns: list[str] | None | Unset
        if isinstance(self.columns, Unset):
            columns = UNSET
        elif isinstance(self.columns, list):
            columns = self.columns

        else:
            columns = self.columns

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters
        if sort_spec is not UNSET:
            field_dict["sort_spec"] = sort_spec
        if columns is not UNSET:
            field_dict["columns"] = columns

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.query_filter_v1 import QueryFilterV1
        from ..models.sort_clause import SortClause

        d = dict(src_dict)
        _filters = d.pop("filters", UNSET)
        filters: list[QueryFilterV1] | Unset = UNSET
        if _filters is not UNSET:
            filters = []
            for filters_item_data in _filters:
                filters_item = QueryFilterV1.from_dict(filters_item_data)

                filters.append(filters_item)

        _sort_spec = d.pop("sort_spec", UNSET)
        sort_spec: list[SortClause] | Unset = UNSET
        if _sort_spec is not UNSET:
            sort_spec = []
            for sort_spec_item_data in _sort_spec:
                sort_spec_item = SortClause.from_dict(sort_spec_item_data)

                sort_spec.append(sort_spec_item)

        def _parse_columns(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                columns_type_0 = cast(list[str], data)

                return columns_type_0
            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        columns = _parse_columns(d.pop("columns", UNSET))

        transaction_rows_request_body = cls(filters=filters, sort_spec=sort_spec, columns=columns)

        transaction_rows_request_body.additional_properties = d
        return transaction_rows_request_body

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
