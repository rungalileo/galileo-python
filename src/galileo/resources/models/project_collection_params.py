from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_bookmark_filter import ProjectBookmarkFilter
    from ..models.project_bookmark_sort import ProjectBookmarkSort
    from ..models.project_created_at_filter import ProjectCreatedAtFilter
    from ..models.project_created_at_sort_v1 import ProjectCreatedAtSortV1
    from ..models.project_creator_filter import ProjectCreatorFilter
    from ..models.project_id_filter import ProjectIDFilter
    from ..models.project_name_filter import ProjectNameFilter
    from ..models.project_name_sort_v1 import ProjectNameSortV1
    from ..models.project_runs_filter import ProjectRunsFilter
    from ..models.project_runs_sort import ProjectRunsSort
    from ..models.project_type_filter import ProjectTypeFilter
    from ..models.project_type_sort import ProjectTypeSort
    from ..models.project_updated_at_filter import ProjectUpdatedAtFilter
    from ..models.project_updated_at_sort_v1 import ProjectUpdatedAtSortV1


T = TypeVar("T", bound="ProjectCollectionParams")


@_attrs_define
class ProjectCollectionParams:
    """
    Attributes
    ----------
        filters (list[ProjectBookmarkFilter | ProjectCreatedAtFilter | ProjectCreatorFilter | ProjectIDFilter |
            ProjectNameFilter | ProjectRunsFilter | ProjectTypeFilter | ProjectUpdatedAtFilter] | Unset):
        sort (None | ProjectBookmarkSort | ProjectCreatedAtSortV1 | ProjectNameSortV1 | ProjectRunsSort |
            ProjectTypeSort | ProjectUpdatedAtSortV1 | Unset):  Default: None.
    """

    filters: (
        list[
            ProjectBookmarkFilter
            | ProjectCreatedAtFilter
            | ProjectCreatorFilter
            | ProjectIDFilter
            | ProjectNameFilter
            | ProjectRunsFilter
            | ProjectTypeFilter
            | ProjectUpdatedAtFilter
        ]
        | Unset
    ) = UNSET
    sort: (
        None
        | ProjectBookmarkSort
        | ProjectCreatedAtSortV1
        | ProjectNameSortV1
        | ProjectRunsSort
        | ProjectTypeSort
        | ProjectUpdatedAtSortV1
        | Unset
    ) = None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.project_bookmark_sort import ProjectBookmarkSort
        from ..models.project_created_at_filter import ProjectCreatedAtFilter
        from ..models.project_created_at_sort_v1 import ProjectCreatedAtSortV1
        from ..models.project_creator_filter import ProjectCreatorFilter
        from ..models.project_id_filter import ProjectIDFilter
        from ..models.project_name_filter import ProjectNameFilter
        from ..models.project_name_sort_v1 import ProjectNameSortV1
        from ..models.project_runs_filter import ProjectRunsFilter
        from ..models.project_runs_sort import ProjectRunsSort
        from ..models.project_type_filter import ProjectTypeFilter
        from ..models.project_type_sort import ProjectTypeSort
        from ..models.project_updated_at_filter import ProjectUpdatedAtFilter
        from ..models.project_updated_at_sort_v1 import ProjectUpdatedAtSortV1

        filters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(
                    filters_item_data,
                    ProjectIDFilter
                    | ProjectNameFilter
                    | ProjectTypeFilter
                    | ProjectCreatorFilter
                    | (ProjectCreatedAtFilter | ProjectUpdatedAtFilter)
                    | ProjectRunsFilter,
                ):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sort: dict[str, Any] | None | Unset
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(
            self.sort,
            ProjectNameSortV1
            | ProjectTypeSort
            | ProjectCreatedAtSortV1
            | ProjectUpdatedAtSortV1
            | (ProjectRunsSort | ProjectBookmarkSort),
        ):
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_bookmark_filter import ProjectBookmarkFilter
        from ..models.project_bookmark_sort import ProjectBookmarkSort
        from ..models.project_created_at_filter import ProjectCreatedAtFilter
        from ..models.project_created_at_sort_v1 import ProjectCreatedAtSortV1
        from ..models.project_creator_filter import ProjectCreatorFilter
        from ..models.project_id_filter import ProjectIDFilter
        from ..models.project_name_filter import ProjectNameFilter
        from ..models.project_name_sort_v1 import ProjectNameSortV1
        from ..models.project_runs_filter import ProjectRunsFilter
        from ..models.project_runs_sort import ProjectRunsSort
        from ..models.project_type_filter import ProjectTypeFilter
        from ..models.project_type_sort import ProjectTypeSort
        from ..models.project_updated_at_filter import ProjectUpdatedAtFilter
        from ..models.project_updated_at_sort_v1 import ProjectUpdatedAtSortV1

        d = dict(src_dict)
        _filters = d.pop("filters", UNSET)
        filters: (
            list[
                ProjectBookmarkFilter
                | ProjectCreatedAtFilter
                | ProjectCreatorFilter
                | ProjectIDFilter
                | ProjectNameFilter
                | ProjectRunsFilter
                | ProjectTypeFilter
                | ProjectUpdatedAtFilter
            ]
            | Unset
        ) = UNSET
        if _filters is not UNSET:
            filters = []
            for filters_item_data in _filters:

                def _parse_filters_item(
                    data: object,
                ) -> (
                    ProjectBookmarkFilter
                    | ProjectCreatedAtFilter
                    | ProjectCreatorFilter
                    | ProjectIDFilter
                    | ProjectNameFilter
                    | ProjectRunsFilter
                    | ProjectTypeFilter
                    | ProjectUpdatedAtFilter
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ProjectIDFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ProjectNameFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ProjectTypeFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ProjectCreatorFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ProjectCreatedAtFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ProjectUpdatedAtFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ProjectRunsFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ProjectBookmarkFilter.from_dict(data)

                filters_item = _parse_filters_item(filters_item_data)

                filters.append(filters_item)

        def _parse_sort(
            data: object,
        ) -> (
            None
            | ProjectBookmarkSort
            | ProjectCreatedAtSortV1
            | ProjectNameSortV1
            | ProjectRunsSort
            | ProjectTypeSort
            | ProjectUpdatedAtSortV1
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ProjectNameSortV1.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ProjectTypeSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ProjectCreatedAtSortV1.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ProjectUpdatedAtSortV1.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ProjectRunsSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ProjectBookmarkSort.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                None
                | ProjectBookmarkSort
                | ProjectCreatedAtSortV1
                | ProjectNameSortV1
                | ProjectRunsSort
                | ProjectTypeSort
                | ProjectUpdatedAtSortV1
                | Unset,
                data,
            )

        sort = _parse_sort(d.pop("sort", UNSET))

        project_collection_params = cls(filters=filters, sort=sort)

        project_collection_params.additional_properties = d
        return project_collection_params

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
