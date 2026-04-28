from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scorer_created_at_filter import ScorerCreatedAtFilter
    from ..models.scorer_creator_filter import ScorerCreatorFilter
    from ..models.scorer_enabled_in_playground_sort import ScorerEnabledInPlaygroundSort
    from ..models.scorer_enabled_in_run_sort import ScorerEnabledInRunSort
    from ..models.scorer_exclude_multimodal_scorers_filter import ScorerExcludeMultimodalScorersFilter
    from ..models.scorer_exclude_slm_scorers_filter import ScorerExcludeSlmScorersFilter
    from ..models.scorer_id_filter import ScorerIDFilter
    from ..models.scorer_label_filter import ScorerLabelFilter
    from ..models.scorer_model_type_filter import ScorerModelTypeFilter
    from ..models.scorer_name_filter import ScorerNameFilter
    from ..models.scorer_name_sort import ScorerNameSort
    from ..models.scorer_scoreable_node_types_filter import ScorerScoreableNodeTypesFilter
    from ..models.scorer_tags_filter import ScorerTagsFilter
    from ..models.scorer_type_filter import ScorerTypeFilter
    from ..models.scorer_updated_at_filter import ScorerUpdatedAtFilter


T = TypeVar("T", bound="ListScorersRequest")


@_attrs_define
class ListScorersRequest:
    """
    Attributes
    ----------
        filters (list[ScorerCreatedAtFilter | ScorerCreatorFilter | ScorerExcludeMultimodalScorersFilter |
            ScorerExcludeSlmScorersFilter | ScorerIDFilter | ScorerLabelFilter | ScorerModelTypeFilter | ScorerNameFilter |
            ScorerScoreableNodeTypesFilter | ScorerTagsFilter | ScorerTypeFilter | ScorerUpdatedAtFilter] | Unset):
        sort (None | ScorerEnabledInPlaygroundSort | ScorerEnabledInRunSort | ScorerNameSort | Unset):
    """

    filters: (
        list[
            ScorerCreatedAtFilter
            | ScorerCreatorFilter
            | ScorerExcludeMultimodalScorersFilter
            | ScorerExcludeSlmScorersFilter
            | ScorerIDFilter
            | ScorerLabelFilter
            | ScorerModelTypeFilter
            | ScorerNameFilter
            | ScorerScoreableNodeTypesFilter
            | ScorerTagsFilter
            | ScorerTypeFilter
            | ScorerUpdatedAtFilter
        ]
        | Unset
    ) = UNSET
    sort: None | ScorerEnabledInPlaygroundSort | ScorerEnabledInRunSort | ScorerNameSort | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.scorer_created_at_filter import ScorerCreatedAtFilter
        from ..models.scorer_creator_filter import ScorerCreatorFilter
        from ..models.scorer_enabled_in_playground_sort import ScorerEnabledInPlaygroundSort
        from ..models.scorer_enabled_in_run_sort import ScorerEnabledInRunSort
        from ..models.scorer_exclude_multimodal_scorers_filter import ScorerExcludeMultimodalScorersFilter
        from ..models.scorer_exclude_slm_scorers_filter import ScorerExcludeSlmScorersFilter
        from ..models.scorer_label_filter import ScorerLabelFilter
        from ..models.scorer_model_type_filter import ScorerModelTypeFilter
        from ..models.scorer_name_filter import ScorerNameFilter
        from ..models.scorer_name_sort import ScorerNameSort
        from ..models.scorer_scoreable_node_types_filter import ScorerScoreableNodeTypesFilter
        from ..models.scorer_tags_filter import ScorerTagsFilter
        from ..models.scorer_type_filter import ScorerTypeFilter
        from ..models.scorer_updated_at_filter import ScorerUpdatedAtFilter

        filters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(
                    filters_item_data,
                    ScorerNameFilter
                    | ScorerTypeFilter
                    | ScorerModelTypeFilter
                    | ScorerExcludeSlmScorersFilter
                    | (ScorerExcludeMultimodalScorersFilter | ScorerTagsFilter)
                    | ScorerCreatorFilter
                    | ScorerCreatedAtFilter
                    | (ScorerUpdatedAtFilter | ScorerLabelFilter | ScorerScoreableNodeTypesFilter),
                ):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sort: dict[str, Any] | None | Unset
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, ScorerNameSort | ScorerEnabledInRunSort | ScorerEnabledInPlaygroundSort):
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
        from ..models.scorer_enabled_in_playground_sort import ScorerEnabledInPlaygroundSort
        from ..models.scorer_enabled_in_run_sort import ScorerEnabledInRunSort
        from ..models.scorer_exclude_multimodal_scorers_filter import ScorerExcludeMultimodalScorersFilter
        from ..models.scorer_exclude_slm_scorers_filter import ScorerExcludeSlmScorersFilter
        from ..models.scorer_id_filter import ScorerIDFilter
        from ..models.scorer_label_filter import ScorerLabelFilter
        from ..models.scorer_model_type_filter import ScorerModelTypeFilter
        from ..models.scorer_name_filter import ScorerNameFilter
        from ..models.scorer_name_sort import ScorerNameSort
        from ..models.scorer_scoreable_node_types_filter import ScorerScoreableNodeTypesFilter
        from ..models.scorer_tags_filter import ScorerTagsFilter
        from ..models.scorer_type_filter import ScorerTypeFilter
        from ..models.scorer_updated_at_filter import ScorerUpdatedAtFilter

        d = dict(src_dict)
        _filters = d.pop("filters", UNSET)
        filters: (
            list[
                ScorerCreatedAtFilter
                | ScorerCreatorFilter
                | ScorerExcludeMultimodalScorersFilter
                | ScorerExcludeSlmScorersFilter
                | ScorerIDFilter
                | ScorerLabelFilter
                | ScorerModelTypeFilter
                | ScorerNameFilter
                | ScorerScoreableNodeTypesFilter
                | ScorerTagsFilter
                | ScorerTypeFilter
                | ScorerUpdatedAtFilter
            ]
            | Unset
        ) = UNSET
        if _filters is not UNSET:
            filters = []
            for filters_item_data in _filters:

                def _parse_filters_item(
                    data: object,
                ) -> (
                    ScorerCreatedAtFilter
                    | ScorerCreatorFilter
                    | ScorerExcludeMultimodalScorersFilter
                    | ScorerExcludeSlmScorersFilter
                    | ScorerIDFilter
                    | ScorerLabelFilter
                    | ScorerModelTypeFilter
                    | ScorerNameFilter
                    | ScorerScoreableNodeTypesFilter
                    | ScorerTagsFilter
                    | ScorerTypeFilter
                    | ScorerUpdatedAtFilter
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerNameFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerTypeFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerModelTypeFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerExcludeSlmScorersFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerExcludeMultimodalScorersFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerTagsFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerCreatorFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerCreatedAtFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerUpdatedAtFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerLabelFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ScorerScoreableNodeTypesFilter.from_dict(data)

                    except:  # noqa: E722
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ScorerIDFilter.from_dict(data)

                filters_item = _parse_filters_item(filters_item_data)

                filters.append(filters_item)

        def _parse_sort(
            data: object,
        ) -> None | ScorerEnabledInPlaygroundSort | ScorerEnabledInRunSort | ScorerNameSort | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ScorerNameSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ScorerEnabledInRunSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ScorerEnabledInPlaygroundSort.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | ScorerEnabledInPlaygroundSort | ScorerEnabledInRunSort | ScorerNameSort | Unset, data)

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
