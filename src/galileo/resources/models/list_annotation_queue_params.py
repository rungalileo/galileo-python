from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_queue_created_at_filter import AnnotationQueueCreatedAtFilter
    from ..models.annotation_queue_created_at_sort import AnnotationQueueCreatedAtSort
    from ..models.annotation_queue_created_by_sort import AnnotationQueueCreatedBySort
    from ..models.annotation_queue_id_filter import AnnotationQueueIDFilter
    from ..models.annotation_queue_name_filter import AnnotationQueueNameFilter
    from ..models.annotation_queue_name_sort import AnnotationQueueNameSort
    from ..models.annotation_queue_num_annotators_filter import AnnotationQueueNumAnnotatorsFilter
    from ..models.annotation_queue_num_annotators_sort import AnnotationQueueNumAnnotatorsSort
    from ..models.annotation_queue_num_log_records_filter import AnnotationQueueNumLogRecordsFilter
    from ..models.annotation_queue_num_log_records_sort import AnnotationQueueNumLogRecordsSort
    from ..models.annotation_queue_num_templates_filter import AnnotationQueueNumTemplatesFilter
    from ..models.annotation_queue_num_templates_sort import AnnotationQueueNumTemplatesSort
    from ..models.annotation_queue_num_users_filter import AnnotationQueueNumUsersFilter
    from ..models.annotation_queue_num_users_sort import AnnotationQueueNumUsersSort
    from ..models.annotation_queue_overall_progress_filter import AnnotationQueueOverallProgressFilter
    from ..models.annotation_queue_overall_progress_sort import AnnotationQueueOverallProgressSort
    from ..models.annotation_queue_project_filter import AnnotationQueueProjectFilter
    from ..models.annotation_queue_updated_at_filter import AnnotationQueueUpdatedAtFilter
    from ..models.annotation_queue_updated_at_sort import AnnotationQueueUpdatedAtSort


T = TypeVar("T", bound="ListAnnotationQueueParams")


@_attrs_define
class ListAnnotationQueueParams:
    """
    Attributes:
        filters (Union[Unset, list[Union['AnnotationQueueCreatedAtFilter', 'AnnotationQueueIDFilter',
            'AnnotationQueueNameFilter', 'AnnotationQueueNumAnnotatorsFilter', 'AnnotationQueueNumLogRecordsFilter',
            'AnnotationQueueNumTemplatesFilter', 'AnnotationQueueNumUsersFilter', 'AnnotationQueueOverallProgressFilter',
            'AnnotationQueueProjectFilter', 'AnnotationQueueUpdatedAtFilter']]]):
        sort (Union['AnnotationQueueCreatedAtSort', 'AnnotationQueueCreatedBySort', 'AnnotationQueueNameSort',
            'AnnotationQueueNumAnnotatorsSort', 'AnnotationQueueNumLogRecordsSort', 'AnnotationQueueNumTemplatesSort',
            'AnnotationQueueNumUsersSort', 'AnnotationQueueOverallProgressSort', 'AnnotationQueueUpdatedAtSort', None,
            Unset]):  Default: None.
    """

    filters: Union[
        Unset,
        list[
            Union[
                "AnnotationQueueCreatedAtFilter",
                "AnnotationQueueIDFilter",
                "AnnotationQueueNameFilter",
                "AnnotationQueueNumAnnotatorsFilter",
                "AnnotationQueueNumLogRecordsFilter",
                "AnnotationQueueNumTemplatesFilter",
                "AnnotationQueueNumUsersFilter",
                "AnnotationQueueOverallProgressFilter",
                "AnnotationQueueProjectFilter",
                "AnnotationQueueUpdatedAtFilter",
            ]
        ],
    ] = UNSET
    sort: Union[
        "AnnotationQueueCreatedAtSort",
        "AnnotationQueueCreatedBySort",
        "AnnotationQueueNameSort",
        "AnnotationQueueNumAnnotatorsSort",
        "AnnotationQueueNumLogRecordsSort",
        "AnnotationQueueNumTemplatesSort",
        "AnnotationQueueNumUsersSort",
        "AnnotationQueueOverallProgressSort",
        "AnnotationQueueUpdatedAtSort",
        None,
        Unset,
    ] = None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.annotation_queue_created_at_filter import AnnotationQueueCreatedAtFilter
        from ..models.annotation_queue_created_at_sort import AnnotationQueueCreatedAtSort
        from ..models.annotation_queue_created_by_sort import AnnotationQueueCreatedBySort
        from ..models.annotation_queue_id_filter import AnnotationQueueIDFilter
        from ..models.annotation_queue_name_filter import AnnotationQueueNameFilter
        from ..models.annotation_queue_name_sort import AnnotationQueueNameSort
        from ..models.annotation_queue_num_annotators_filter import AnnotationQueueNumAnnotatorsFilter
        from ..models.annotation_queue_num_annotators_sort import AnnotationQueueNumAnnotatorsSort
        from ..models.annotation_queue_num_log_records_filter import AnnotationQueueNumLogRecordsFilter
        from ..models.annotation_queue_num_log_records_sort import AnnotationQueueNumLogRecordsSort
        from ..models.annotation_queue_num_templates_sort import AnnotationQueueNumTemplatesSort
        from ..models.annotation_queue_num_users_filter import AnnotationQueueNumUsersFilter
        from ..models.annotation_queue_num_users_sort import AnnotationQueueNumUsersSort
        from ..models.annotation_queue_overall_progress_filter import AnnotationQueueOverallProgressFilter
        from ..models.annotation_queue_overall_progress_sort import AnnotationQueueOverallProgressSort
        from ..models.annotation_queue_project_filter import AnnotationQueueProjectFilter
        from ..models.annotation_queue_updated_at_filter import AnnotationQueueUpdatedAtFilter
        from ..models.annotation_queue_updated_at_sort import AnnotationQueueUpdatedAtSort

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(filters_item_data, AnnotationQueueIDFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, AnnotationQueueNameFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, AnnotationQueueProjectFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, AnnotationQueueCreatedAtFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, AnnotationQueueUpdatedAtFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, AnnotationQueueNumLogRecordsFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, AnnotationQueueNumAnnotatorsFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, AnnotationQueueNumUsersFilter):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, AnnotationQueueOverallProgressFilter):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, AnnotationQueueNameSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, AnnotationQueueCreatedAtSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, AnnotationQueueUpdatedAtSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, AnnotationQueueCreatedBySort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, AnnotationQueueNumUsersSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, AnnotationQueueNumLogRecordsSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, AnnotationQueueNumTemplatesSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, AnnotationQueueNumAnnotatorsSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, AnnotationQueueOverallProgressSort):
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
        from ..models.annotation_queue_created_at_filter import AnnotationQueueCreatedAtFilter
        from ..models.annotation_queue_created_at_sort import AnnotationQueueCreatedAtSort
        from ..models.annotation_queue_created_by_sort import AnnotationQueueCreatedBySort
        from ..models.annotation_queue_id_filter import AnnotationQueueIDFilter
        from ..models.annotation_queue_name_filter import AnnotationQueueNameFilter
        from ..models.annotation_queue_name_sort import AnnotationQueueNameSort
        from ..models.annotation_queue_num_annotators_filter import AnnotationQueueNumAnnotatorsFilter
        from ..models.annotation_queue_num_annotators_sort import AnnotationQueueNumAnnotatorsSort
        from ..models.annotation_queue_num_log_records_filter import AnnotationQueueNumLogRecordsFilter
        from ..models.annotation_queue_num_log_records_sort import AnnotationQueueNumLogRecordsSort
        from ..models.annotation_queue_num_templates_filter import AnnotationQueueNumTemplatesFilter
        from ..models.annotation_queue_num_templates_sort import AnnotationQueueNumTemplatesSort
        from ..models.annotation_queue_num_users_filter import AnnotationQueueNumUsersFilter
        from ..models.annotation_queue_num_users_sort import AnnotationQueueNumUsersSort
        from ..models.annotation_queue_overall_progress_filter import AnnotationQueueOverallProgressFilter
        from ..models.annotation_queue_overall_progress_sort import AnnotationQueueOverallProgressSort
        from ..models.annotation_queue_project_filter import AnnotationQueueProjectFilter
        from ..models.annotation_queue_updated_at_filter import AnnotationQueueUpdatedAtFilter
        from ..models.annotation_queue_updated_at_sort import AnnotationQueueUpdatedAtSort

        d = dict(src_dict)
        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(
                data: object,
            ) -> Union[
                "AnnotationQueueCreatedAtFilter",
                "AnnotationQueueIDFilter",
                "AnnotationQueueNameFilter",
                "AnnotationQueueNumAnnotatorsFilter",
                "AnnotationQueueNumLogRecordsFilter",
                "AnnotationQueueNumTemplatesFilter",
                "AnnotationQueueNumUsersFilter",
                "AnnotationQueueOverallProgressFilter",
                "AnnotationQueueProjectFilter",
                "AnnotationQueueUpdatedAtFilter",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = AnnotationQueueIDFilter.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_1 = AnnotationQueueNameFilter.from_dict(data)

                    return filters_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_2 = AnnotationQueueProjectFilter.from_dict(data)

                    return filters_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_3 = AnnotationQueueCreatedAtFilter.from_dict(data)

                    return filters_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_4 = AnnotationQueueUpdatedAtFilter.from_dict(data)

                    return filters_item_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_5 = AnnotationQueueNumLogRecordsFilter.from_dict(data)

                    return filters_item_type_5
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_6 = AnnotationQueueNumAnnotatorsFilter.from_dict(data)

                    return filters_item_type_6
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_7 = AnnotationQueueNumUsersFilter.from_dict(data)

                    return filters_item_type_7
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_8 = AnnotationQueueOverallProgressFilter.from_dict(data)

                    return filters_item_type_8
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_9 = AnnotationQueueNumTemplatesFilter.from_dict(data)

                return filters_item_type_9

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        def _parse_sort(
            data: object,
        ) -> Union[
            "AnnotationQueueCreatedAtSort",
            "AnnotationQueueCreatedBySort",
            "AnnotationQueueNameSort",
            "AnnotationQueueNumAnnotatorsSort",
            "AnnotationQueueNumLogRecordsSort",
            "AnnotationQueueNumTemplatesSort",
            "AnnotationQueueNumUsersSort",
            "AnnotationQueueOverallProgressSort",
            "AnnotationQueueUpdatedAtSort",
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
                sort_type_0_type_0 = AnnotationQueueNameSort.from_dict(data)

                return sort_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_1 = AnnotationQueueCreatedAtSort.from_dict(data)

                return sort_type_0_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_2 = AnnotationQueueUpdatedAtSort.from_dict(data)

                return sort_type_0_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_3 = AnnotationQueueCreatedBySort.from_dict(data)

                return sort_type_0_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_4 = AnnotationQueueNumUsersSort.from_dict(data)

                return sort_type_0_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_5 = AnnotationQueueNumLogRecordsSort.from_dict(data)

                return sort_type_0_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_6 = AnnotationQueueNumTemplatesSort.from_dict(data)

                return sort_type_0_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_7 = AnnotationQueueNumAnnotatorsSort.from_dict(data)

                return sort_type_0_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_8 = AnnotationQueueOverallProgressSort.from_dict(data)

                return sort_type_0_type_8
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "AnnotationQueueCreatedAtSort",
                    "AnnotationQueueCreatedBySort",
                    "AnnotationQueueNameSort",
                    "AnnotationQueueNumAnnotatorsSort",
                    "AnnotationQueueNumLogRecordsSort",
                    "AnnotationQueueNumTemplatesSort",
                    "AnnotationQueueNumUsersSort",
                    "AnnotationQueueOverallProgressSort",
                    "AnnotationQueueUpdatedAtSort",
                    None,
                    Unset,
                ],
                data,
            )

        sort = _parse_sort(d.pop("sort", UNSET))

        list_annotation_queue_params = cls(filters=filters, sort=sort)

        list_annotation_queue_params.additional_properties = d
        return list_annotation_queue_params

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
