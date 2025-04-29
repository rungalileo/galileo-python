from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_created_at_filter import ProjectCreatedAtFilter
    from ..models.project_created_at_sort import ProjectCreatedAtSort
    from ..models.project_creator_filter import ProjectCreatorFilter
    from ..models.project_name_filter import ProjectNameFilter
    from ..models.project_name_sort import ProjectNameSort
    from ..models.project_num_experiments_filter import ProjectNumExperimentsFilter
    from ..models.project_num_experiments_sort import ProjectNumExperimentsSort
    from ..models.project_num_logstreams_filter import ProjectNumLogstreamsFilter
    from ..models.project_num_logstreams_sort import ProjectNumLogstreamsSort
    from ..models.project_updated_at_filter import ProjectUpdatedAtFilter
    from ..models.project_updated_at_sort import ProjectUpdatedAtSort


T = TypeVar("T", bound="ProjectCollectionParamsV2")


@_attrs_define
class ProjectCollectionParamsV2:
    """
    Attributes:
        filters (Union[Unset, list[Union['ProjectCreatedAtFilter', 'ProjectCreatorFilter', 'ProjectNameFilter',
            'ProjectNumExperimentsFilter', 'ProjectNumLogstreamsFilter', 'ProjectUpdatedAtFilter']]]):
        sort (Union['ProjectCreatedAtSort', 'ProjectNameSort', 'ProjectNumExperimentsSort', 'ProjectNumLogstreamsSort',
            'ProjectUpdatedAtSort', None, Unset]):  Default: None.
    """

    filters: Union[
        Unset,
        list[
            Union[
                "ProjectCreatedAtFilter",
                "ProjectCreatorFilter",
                "ProjectNameFilter",
                "ProjectNumExperimentsFilter",
                "ProjectNumLogstreamsFilter",
                "ProjectUpdatedAtFilter",
            ]
        ],
    ] = UNSET
    sort: Union[
        "ProjectCreatedAtSort",
        "ProjectNameSort",
        "ProjectNumExperimentsSort",
        "ProjectNumLogstreamsSort",
        "ProjectUpdatedAtSort",
        None,
        Unset,
    ] = None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.project_created_at_filter import ProjectCreatedAtFilter
        from ..models.project_created_at_sort import ProjectCreatedAtSort
        from ..models.project_creator_filter import ProjectCreatorFilter
        from ..models.project_name_filter import ProjectNameFilter
        from ..models.project_name_sort import ProjectNameSort
        from ..models.project_num_experiments_sort import ProjectNumExperimentsSort
        from ..models.project_num_logstreams_filter import ProjectNumLogstreamsFilter
        from ..models.project_num_logstreams_sort import ProjectNumLogstreamsSort
        from ..models.project_updated_at_filter import ProjectUpdatedAtFilter
        from ..models.project_updated_at_sort import ProjectUpdatedAtSort

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(filters_item_data, ProjectNameFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, ProjectCreatorFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, ProjectCreatedAtFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, ProjectUpdatedAtFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, ProjectNumLogstreamsFilter):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, ProjectNameSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, ProjectCreatedAtSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, ProjectUpdatedAtSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, ProjectNumLogstreamsSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, ProjectNumExperimentsSort):
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
        from ..models.project_created_at_filter import ProjectCreatedAtFilter
        from ..models.project_created_at_sort import ProjectCreatedAtSort
        from ..models.project_creator_filter import ProjectCreatorFilter
        from ..models.project_name_filter import ProjectNameFilter
        from ..models.project_name_sort import ProjectNameSort
        from ..models.project_num_experiments_filter import ProjectNumExperimentsFilter
        from ..models.project_num_experiments_sort import ProjectNumExperimentsSort
        from ..models.project_num_logstreams_filter import ProjectNumLogstreamsFilter
        from ..models.project_num_logstreams_sort import ProjectNumLogstreamsSort
        from ..models.project_updated_at_filter import ProjectUpdatedAtFilter
        from ..models.project_updated_at_sort import ProjectUpdatedAtSort

        d = src_dict.copy()
        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(
                data: object,
            ) -> Union[
                "ProjectCreatedAtFilter",
                "ProjectCreatorFilter",
                "ProjectNameFilter",
                "ProjectNumExperimentsFilter",
                "ProjectNumLogstreamsFilter",
                "ProjectUpdatedAtFilter",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = ProjectNameFilter.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_1 = ProjectCreatorFilter.from_dict(data)

                    return filters_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_2 = ProjectCreatedAtFilter.from_dict(data)

                    return filters_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_3 = ProjectUpdatedAtFilter.from_dict(data)

                    return filters_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_4 = ProjectNumLogstreamsFilter.from_dict(data)

                    return filters_item_type_4
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_5 = ProjectNumExperimentsFilter.from_dict(data)

                return filters_item_type_5

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        def _parse_sort(
            data: object,
        ) -> Union[
            "ProjectCreatedAtSort",
            "ProjectNameSort",
            "ProjectNumExperimentsSort",
            "ProjectNumLogstreamsSort",
            "ProjectUpdatedAtSort",
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
                sort_type_0_type_0 = ProjectNameSort.from_dict(data)

                return sort_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_1 = ProjectCreatedAtSort.from_dict(data)

                return sort_type_0_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_2 = ProjectUpdatedAtSort.from_dict(data)

                return sort_type_0_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_3 = ProjectNumLogstreamsSort.from_dict(data)

                return sort_type_0_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_4 = ProjectNumExperimentsSort.from_dict(data)

                return sort_type_0_type_4
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "ProjectCreatedAtSort",
                    "ProjectNameSort",
                    "ProjectNumExperimentsSort",
                    "ProjectNumLogstreamsSort",
                    "ProjectUpdatedAtSort",
                    None,
                    Unset,
                ],
                data,
            )

        sort = _parse_sort(d.pop("sort", UNSET))

        project_collection_params_v2 = cls(filters=filters, sort=sort)

        project_collection_params_v2.additional_properties = d
        return project_collection_params_v2

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
