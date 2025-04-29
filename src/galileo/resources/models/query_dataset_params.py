from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_content_filter import DatasetContentFilter
    from ..models.dataset_content_sort_clause import DatasetContentSortClause


T = TypeVar("T", bound="QueryDatasetParams")


@_attrs_define
class QueryDatasetParams:
    """
    Attributes:
        filters (Union[Unset, list['DatasetContentFilter']]):
        sort (Union['DatasetContentSortClause', None, Unset]):
    """

    filters: Union[Unset, list["DatasetContentFilter"]] = UNSET
    sort: Union["DatasetContentSortClause", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_content_sort_clause import DatasetContentSortClause

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, DatasetContentSortClause):
            sort = self.sort.to_dict()
        else:
            sort = self.sort

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters
        if sort is not UNSET:
            field_dict["sort"] = sort

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dataset_content_filter import DatasetContentFilter
        from ..models.dataset_content_sort_clause import DatasetContentSortClause

        d = src_dict.copy()
        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:
            filters_item = DatasetContentFilter.from_dict(filters_item_data)

            filters.append(filters_item)

        def _parse_sort(data: object) -> Union["DatasetContentSortClause", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0 = DatasetContentSortClause.from_dict(data)

                return sort_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatasetContentSortClause", None, Unset], data)

        sort = _parse_sort(d.pop("sort", UNSET))

        query_dataset_params = cls(filters=filters, sort=sort)

        query_dataset_params.additional_properties = d
        return query_dataset_params

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
