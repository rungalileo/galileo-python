from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.and_node_log_records_filter import AndNodeLogRecordsFilter
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.not_node_log_records_filter import NotNodeLogRecordsFilter
    from ..models.or_node_log_records_filter import OrNodeLogRecordsFilter


T = TypeVar("T", bound="AnnotationQueueCountRequest")


@_attrs_define
class AnnotationQueueCountRequest:
    """
    Attributes
    ----------
        filter_tree (Union['AndNodeLogRecordsFilter', 'FilterLeafLogRecordsFilter', 'NotNodeLogRecordsFilter',
            'OrNodeLogRecordsFilter', None, Unset]):
    """

    filter_tree: Union[
        "AndNodeLogRecordsFilter",
        "FilterLeafLogRecordsFilter",
        "NotNodeLogRecordsFilter",
        "OrNodeLogRecordsFilter",
        None,
        Unset,
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node_log_records_filter import AndNodeLogRecordsFilter
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.not_node_log_records_filter import NotNodeLogRecordsFilter
        from ..models.or_node_log_records_filter import OrNodeLogRecordsFilter

        filter_tree: None | Unset | dict[str, Any]
        if isinstance(self.filter_tree, Unset):
            filter_tree = UNSET
        elif isinstance(
            self.filter_tree,
            FilterLeafLogRecordsFilter | AndNodeLogRecordsFilter | OrNodeLogRecordsFilter | NotNodeLogRecordsFilter,
        ):
            filter_tree = self.filter_tree.to_dict()
        else:
            filter_tree = self.filter_tree

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_tree is not UNSET:
            field_dict["filter_tree"] = filter_tree

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node_log_records_filter import AndNodeLogRecordsFilter
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.not_node_log_records_filter import NotNodeLogRecordsFilter
        from ..models.or_node_log_records_filter import OrNodeLogRecordsFilter

        d = dict(src_dict)

        def _parse_filter_tree(
            data: object,
        ) -> Union[
            "AndNodeLogRecordsFilter",
            "FilterLeafLogRecordsFilter",
            "NotNodeLogRecordsFilter",
            "OrNodeLogRecordsFilter",
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
                return FilterLeafLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AndNodeLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return OrNodeLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return NotNodeLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "AndNodeLogRecordsFilter",
                    "FilterLeafLogRecordsFilter",
                    "NotNodeLogRecordsFilter",
                    "OrNodeLogRecordsFilter",
                    None,
                    Unset,
                ],
                data,
            )

        filter_tree = _parse_filter_tree(d.pop("filter_tree", UNSET))

        annotation_queue_count_request = cls(filter_tree=filter_tree)

        annotation_queue_count_request.additional_properties = d
        return annotation_queue_count_request

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
