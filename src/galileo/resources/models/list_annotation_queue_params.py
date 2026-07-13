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
    Attributes
    ----------
        filters (Union[Unset, list[Union['AnnotationQueueCreatedAtFilter', 'AnnotationQueueIDFilter',
            'AnnotationQueueNameFilter', 'AnnotationQueueNumAnnotatorsFilter', 'AnnotationQueueNumLogRecordsFilter',
            'AnnotationQueueNumTemplatesFilter', 'AnnotationQueueNumUsersFilter', 'AnnotationQueueOverallProgressFilter',
            'AnnotationQueueProjectFilter', 'AnnotationQueueUpdatedAtFilter']]]):
        sort (Union['AnnotationQueueCreatedAtSort', 'AnnotationQueueCreatedBySort', 'AnnotationQueueNameSort',
            'AnnotationQueueNumAnnotatorsSort', 'AnnotationQueueNumLogRecordsSort', 'AnnotationQueueNumTemplatesSort',
            'AnnotationQueueNumUsersSort', 'AnnotationQueueOverallProgressSort', 'AnnotationQueueUpdatedAtSort', None,
            Unset]):  Default: None.
    """

    filters: (
        Unset
        | list[
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
        ]
    ) = UNSET
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

        filters: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(
                    filters_item_data,
                    AnnotationQueueIDFilter
                    | AnnotationQueueNameFilter
                    | AnnotationQueueProjectFilter
                    | AnnotationQueueCreatedAtFilter
                    | (AnnotationQueueUpdatedAtFilter | AnnotationQueueNumLogRecordsFilter)
                    | AnnotationQueueNumAnnotatorsFilter
                    | AnnotationQueueNumUsersFilter
                    | AnnotationQueueOverallProgressFilter,
                ):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sort: None | Unset | dict[str, Any]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(
            self.sort,
            AnnotationQueueNameSort
            | AnnotationQueueCreatedAtSort
            | AnnotationQueueUpdatedAtSort
            | AnnotationQueueCreatedBySort
            | (AnnotationQueueNumUsersSort | AnnotationQueueNumLogRecordsSort)
            | AnnotationQueueNumTemplatesSort
            | AnnotationQueueNumAnnotatorsSort
            | AnnotationQueueOverallProgressSort,
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
                    return AnnotationQueueIDFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return AnnotationQueueNameFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return AnnotationQueueProjectFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return AnnotationQueueCreatedAtFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return AnnotationQueueUpdatedAtFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return AnnotationQueueNumLogRecordsFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return AnnotationQueueNumAnnotatorsFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return AnnotationQueueNumUsersFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return AnnotationQueueOverallProgressFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueNumTemplatesFilter.from_dict(data)

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
                return AnnotationQueueNameSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueCreatedAtSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueUpdatedAtSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueCreatedBySort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueNumUsersSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueNumLogRecordsSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueNumTemplatesSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueNumAnnotatorsSort.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueOverallProgressSort.from_dict(data)

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
