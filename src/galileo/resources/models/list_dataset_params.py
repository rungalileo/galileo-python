from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_created_at_sort import DatasetCreatedAtSort
    from ..models.dataset_last_edited_by_user_at_sort import DatasetLastEditedByUserAtSort
    from ..models.dataset_name_filter import DatasetNameFilter
    from ..models.dataset_name_sort import DatasetNameSort
    from ..models.dataset_project_last_used_at_sort import DatasetProjectLastUsedAtSort
    from ..models.dataset_projects_sort import DatasetProjectsSort
    from ..models.dataset_rows_sort import DatasetRowsSort
    from ..models.dataset_updated_at_sort import DatasetUpdatedAtSort
    from ..models.dataset_used_in_project_filter import DatasetUsedInProjectFilter


T = TypeVar("T", bound="ListDatasetParams")


@_attrs_define
class ListDatasetParams:
    """
    Attributes:
        filters (Union[Unset, list[Union['DatasetNameFilter', 'DatasetUsedInProjectFilter']]]):
        sort (Union['DatasetCreatedAtSort', 'DatasetLastEditedByUserAtSort', 'DatasetNameSort',
            'DatasetProjectLastUsedAtSort', 'DatasetProjectsSort', 'DatasetRowsSort', 'DatasetUpdatedAtSort', None, Unset]):
            Default: None.
    """

    filters: Union[Unset, list[Union["DatasetNameFilter", "DatasetUsedInProjectFilter"]]] = UNSET
    sort: Union[
        "DatasetCreatedAtSort",
        "DatasetLastEditedByUserAtSort",
        "DatasetNameSort",
        "DatasetProjectLastUsedAtSort",
        "DatasetProjectsSort",
        "DatasetRowsSort",
        "DatasetUpdatedAtSort",
        None,
        Unset,
    ] = None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_created_at_sort import DatasetCreatedAtSort
        from ..models.dataset_last_edited_by_user_at_sort import DatasetLastEditedByUserAtSort
        from ..models.dataset_name_filter import DatasetNameFilter
        from ..models.dataset_name_sort import DatasetNameSort
        from ..models.dataset_project_last_used_at_sort import DatasetProjectLastUsedAtSort
        from ..models.dataset_projects_sort import DatasetProjectsSort
        from ..models.dataset_rows_sort import DatasetRowsSort
        from ..models.dataset_updated_at_sort import DatasetUpdatedAtSort

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(filters_item_data, DatasetNameFilter):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, DatasetNameSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, DatasetCreatedAtSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, DatasetUpdatedAtSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, DatasetProjectLastUsedAtSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, DatasetProjectsSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, DatasetRowsSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, DatasetLastEditedByUserAtSort):
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
        from ..models.dataset_created_at_sort import DatasetCreatedAtSort
        from ..models.dataset_last_edited_by_user_at_sort import DatasetLastEditedByUserAtSort
        from ..models.dataset_name_filter import DatasetNameFilter
        from ..models.dataset_name_sort import DatasetNameSort
        from ..models.dataset_project_last_used_at_sort import DatasetProjectLastUsedAtSort
        from ..models.dataset_projects_sort import DatasetProjectsSort
        from ..models.dataset_rows_sort import DatasetRowsSort
        from ..models.dataset_updated_at_sort import DatasetUpdatedAtSort
        from ..models.dataset_used_in_project_filter import DatasetUsedInProjectFilter

        d = src_dict.copy()
        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(data: object) -> Union["DatasetNameFilter", "DatasetUsedInProjectFilter"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = DatasetNameFilter.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_1 = DatasetUsedInProjectFilter.from_dict(data)

                return filters_item_type_1

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        def _parse_sort(
            data: object,
        ) -> Union[
            "DatasetCreatedAtSort",
            "DatasetLastEditedByUserAtSort",
            "DatasetNameSort",
            "DatasetProjectLastUsedAtSort",
            "DatasetProjectsSort",
            "DatasetRowsSort",
            "DatasetUpdatedAtSort",
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_0 = DatasetNameSort.from_dict(data)

                return sort_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_1 = DatasetCreatedAtSort.from_dict(data)

                return sort_type_0_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_2 = DatasetUpdatedAtSort.from_dict(data)

                return sort_type_0_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_3 = DatasetProjectLastUsedAtSort.from_dict(data)

                return sort_type_0_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_4 = DatasetProjectsSort.from_dict(data)

                return sort_type_0_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_5 = DatasetRowsSort.from_dict(data)

                return sort_type_0_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_6 = DatasetLastEditedByUserAtSort.from_dict(data)

                return sort_type_0_type_6
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "DatasetCreatedAtSort",
                    "DatasetLastEditedByUserAtSort",
                    "DatasetNameSort",
                    "DatasetProjectLastUsedAtSort",
                    "DatasetProjectsSort",
                    "DatasetRowsSort",
                    "DatasetUpdatedAtSort",
                    None,
                    Unset,
                ],
                data,
            )

        sort = _parse_sort(d.pop("sort", UNSET))

        list_dataset_params = cls(filters=filters, sort=sort)

        list_dataset_params.additional_properties = d
        return list_dataset_params

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
