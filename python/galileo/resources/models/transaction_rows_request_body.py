from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
        columns (Union[None, Unset, list[str]]):
        filters (Union[Unset, list['QueryFilterV1']]):
        sort_spec (Union[Unset, list['SortClause']]):
    """

    columns: Union[None, Unset, list[str]] = UNSET
    filters: Union[Unset, list["QueryFilterV1"]] = UNSET
    sort_spec: Union[Unset, list["SortClause"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        columns: Union[None, Unset, list[str]]
        if isinstance(self.columns, Unset):
            columns = UNSET
        elif isinstance(self.columns, list):
            columns = self.columns

        else:
            columns = self.columns

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)

        sort_spec: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sort_spec, Unset):
            sort_spec = []
            for sort_spec_item_data in self.sort_spec:
                sort_spec_item = sort_spec_item_data.to_dict()
                sort_spec.append(sort_spec_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if columns is not UNSET:
            field_dict["columns"] = columns
        if filters is not UNSET:
            field_dict["filters"] = filters
        if sort_spec is not UNSET:
            field_dict["sort_spec"] = sort_spec

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.query_filter_v1 import QueryFilterV1
        from ..models.sort_clause import SortClause

        d = src_dict.copy()

        def _parse_columns(data: object) -> Union[None, Unset, list[str]]:
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
            return cast(Union[None, Unset, list[str]], data)

        columns = _parse_columns(d.pop("columns", UNSET))

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:
            filters_item = QueryFilterV1.from_dict(filters_item_data)

            filters.append(filters_item)

        sort_spec = []
        _sort_spec = d.pop("sort_spec", UNSET)
        for sort_spec_item_data in _sort_spec or []:
            sort_spec_item = SortClause.from_dict(sort_spec_item_data)

            sort_spec.append(sort_spec_item)

        transaction_rows_request_body = cls(columns=columns, filters=filters, sort_spec=sort_spec)

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
