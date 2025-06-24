from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.prompt_template_created_at_sort import PromptTemplateCreatedAtSort
    from ..models.prompt_template_created_by_filter import PromptTemplateCreatedByFilter
    from ..models.prompt_template_name_filter import PromptTemplateNameFilter
    from ..models.prompt_template_name_sort import PromptTemplateNameSort
    from ..models.prompt_template_updated_at_sort import PromptTemplateUpdatedAtSort
    from ..models.prompt_template_used_in_project_filter import PromptTemplateUsedInProjectFilter


T = TypeVar("T", bound="ListPromptTemplateParams")


@_attrs_define
class ListPromptTemplateParams:
    """
    Attributes:
        filters (Union[Unset, list[Union['PromptTemplateCreatedByFilter', 'PromptTemplateNameFilter',
            'PromptTemplateUsedInProjectFilter']]]):
        sort (Union['PromptTemplateCreatedAtSort', 'PromptTemplateNameSort', 'PromptTemplateUpdatedAtSort', None,
            Unset]):  Default: None.
    """

    filters: Union[
        Unset,
        list[Union["PromptTemplateCreatedByFilter", "PromptTemplateNameFilter", "PromptTemplateUsedInProjectFilter"]],
    ] = UNSET
    sort: Union["PromptTemplateCreatedAtSort", "PromptTemplateNameSort", "PromptTemplateUpdatedAtSort", None, Unset] = (
        None
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.prompt_template_created_at_sort import PromptTemplateCreatedAtSort
        from ..models.prompt_template_created_by_filter import PromptTemplateCreatedByFilter
        from ..models.prompt_template_name_filter import PromptTemplateNameFilter
        from ..models.prompt_template_name_sort import PromptTemplateNameSort
        from ..models.prompt_template_updated_at_sort import PromptTemplateUpdatedAtSort

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(filters_item_data, PromptTemplateNameFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, PromptTemplateCreatedByFilter):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, PromptTemplateNameSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, PromptTemplateCreatedAtSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, PromptTemplateUpdatedAtSort):
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
        from ..models.prompt_template_created_at_sort import PromptTemplateCreatedAtSort
        from ..models.prompt_template_created_by_filter import PromptTemplateCreatedByFilter
        from ..models.prompt_template_name_filter import PromptTemplateNameFilter
        from ..models.prompt_template_name_sort import PromptTemplateNameSort
        from ..models.prompt_template_updated_at_sort import PromptTemplateUpdatedAtSort
        from ..models.prompt_template_used_in_project_filter import PromptTemplateUsedInProjectFilter

        d = dict(src_dict)
        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(
                data: object,
            ) -> Union[
                "PromptTemplateCreatedByFilter", "PromptTemplateNameFilter", "PromptTemplateUsedInProjectFilter"
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = PromptTemplateNameFilter.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_1 = PromptTemplateCreatedByFilter.from_dict(data)

                    return filters_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_2 = PromptTemplateUsedInProjectFilter.from_dict(data)

                return filters_item_type_2

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        def _parse_sort(
            data: object,
        ) -> Union["PromptTemplateCreatedAtSort", "PromptTemplateNameSort", "PromptTemplateUpdatedAtSort", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_0 = PromptTemplateNameSort.from_dict(data)

                return sort_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_1 = PromptTemplateCreatedAtSort.from_dict(data)

                return sort_type_0_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_2 = PromptTemplateUpdatedAtSort.from_dict(data)

                return sort_type_0_type_2
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "PromptTemplateCreatedAtSort", "PromptTemplateNameSort", "PromptTemplateUpdatedAtSort", None, Unset
                ],
                data,
            )

        sort = _parse_sort(d.pop("sort", UNSET))

        list_prompt_template_params = cls(filters=filters, sort=sort)

        list_prompt_template_params.additional_properties = d
        return list_prompt_template_params

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
