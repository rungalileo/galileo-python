from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scorer_created_at_filter import ScorerCreatedAtFilter
    from ..models.scorer_creator_filter import ScorerCreatorFilter
    from ..models.scorer_enabled_in_run_sort import ScorerEnabledInRunSort
    from ..models.scorer_model_type_filter import ScorerModelTypeFilter
    from ..models.scorer_name_filter import ScorerNameFilter
    from ..models.scorer_name_sort import ScorerNameSort
    from ..models.scorer_tags_filter import ScorerTagsFilter
    from ..models.scorer_type_filter import ScorerTypeFilter
    from ..models.scorer_updated_at_filter import ScorerUpdatedAtFilter


T = TypeVar("T", bound="ListScorersRequest")


@_attrs_define
class ListScorersRequest:
    """
    Attributes:
        filters (Union[Unset, list[Union['ScorerCreatedAtFilter', 'ScorerCreatorFilter', 'ScorerModelTypeFilter',
            'ScorerNameFilter', 'ScorerTagsFilter', 'ScorerTypeFilter', 'ScorerUpdatedAtFilter']]]):
        sort (Union['ScorerEnabledInRunSort', 'ScorerNameSort', None, Unset]):
    """

    filters: Union[
        Unset,
        list[
            Union[
                "ScorerCreatedAtFilter",
                "ScorerCreatorFilter",
                "ScorerModelTypeFilter",
                "ScorerNameFilter",
                "ScorerTagsFilter",
                "ScorerTypeFilter",
                "ScorerUpdatedAtFilter",
            ]
        ],
    ] = UNSET
    sort: Union["ScorerEnabledInRunSort", "ScorerNameSort", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.scorer_created_at_filter import ScorerCreatedAtFilter
        from ..models.scorer_creator_filter import ScorerCreatorFilter
        from ..models.scorer_enabled_in_run_sort import ScorerEnabledInRunSort
        from ..models.scorer_model_type_filter import ScorerModelTypeFilter
        from ..models.scorer_name_filter import ScorerNameFilter
        from ..models.scorer_name_sort import ScorerNameSort
        from ..models.scorer_tags_filter import ScorerTagsFilter
        from ..models.scorer_type_filter import ScorerTypeFilter

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(filters_item_data, ScorerNameFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, ScorerTypeFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, ScorerModelTypeFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, ScorerTagsFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, ScorerCreatorFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, ScorerCreatedAtFilter):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, ScorerNameSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, ScorerEnabledInRunSort):
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
        from ..models.scorer_created_at_filter import ScorerCreatedAtFilter
        from ..models.scorer_creator_filter import ScorerCreatorFilter
        from ..models.scorer_enabled_in_run_sort import ScorerEnabledInRunSort
        from ..models.scorer_model_type_filter import ScorerModelTypeFilter
        from ..models.scorer_name_filter import ScorerNameFilter
        from ..models.scorer_name_sort import ScorerNameSort
        from ..models.scorer_tags_filter import ScorerTagsFilter
        from ..models.scorer_type_filter import ScorerTypeFilter
        from ..models.scorer_updated_at_filter import ScorerUpdatedAtFilter

        d = dict(src_dict)
        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(
                data: object,
            ) -> Union[
                "ScorerCreatedAtFilter",
                "ScorerCreatorFilter",
                "ScorerModelTypeFilter",
                "ScorerNameFilter",
                "ScorerTagsFilter",
                "ScorerTypeFilter",
                "ScorerUpdatedAtFilter",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = ScorerNameFilter.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_1 = ScorerTypeFilter.from_dict(data)

                    return filters_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_2 = ScorerModelTypeFilter.from_dict(data)

                    return filters_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_3 = ScorerTagsFilter.from_dict(data)

                    return filters_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_4 = ScorerCreatorFilter.from_dict(data)

                    return filters_item_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_5 = ScorerCreatedAtFilter.from_dict(data)

                    return filters_item_type_5
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_6 = ScorerUpdatedAtFilter.from_dict(data)

                return filters_item_type_6

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        def _parse_sort(data: object) -> Union["ScorerEnabledInRunSort", "ScorerNameSort", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_0 = ScorerNameSort.from_dict(data)

                return sort_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_1 = ScorerEnabledInRunSort.from_dict(data)

                return sort_type_0_type_1
            except:  # noqa: E722
                pass
            return cast(Union["ScorerEnabledInRunSort", "ScorerNameSort", None, Unset], data)

        sort = _parse_sort(d.pop("sort", UNSET))

        list_scorers_request = cls(filters=filters, sort=sort)

        list_scorers_request.additional_properties = d
        return list_scorers_request

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
