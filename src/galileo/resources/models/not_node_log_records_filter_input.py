from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput


T = TypeVar("T", bound="NotNodeLogRecordsFilterInput")


@_attrs_define
class NotNodeLogRecordsFilterInput:
    """
    Attributes:
        not_ (AndNodeLogRecordsFilterInput | FilterLeafLogRecordsFilter | NotNodeLogRecordsFilterInput |
            OrNodeLogRecordsFilterInput):
    """

    not_: (
        AndNodeLogRecordsFilterInput
        | FilterLeafLogRecordsFilter
        | NotNodeLogRecordsFilterInput
        | OrNodeLogRecordsFilterInput
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput

        not_: dict[str, Any]
        if isinstance(self.not_, FilterLeafLogRecordsFilter):
            not_ = self.not_.to_dict()
        elif isinstance(self.not_, AndNodeLogRecordsFilterInput):
            not_ = self.not_.to_dict()
        elif isinstance(self.not_, OrNodeLogRecordsFilterInput):
            not_ = self.not_.to_dict()
        else:
            not_ = self.not_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"not": not_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput

        d = dict(src_dict)

        def _parse_not_(
            data: object,
        ) -> (
            AndNodeLogRecordsFilterInput
            | FilterLeafLogRecordsFilter
            | NotNodeLogRecordsFilterInput
            | OrNodeLogRecordsFilterInput
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                not_type_0 = FilterLeafLogRecordsFilter.from_dict(data)

                return not_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                not_type_1 = AndNodeLogRecordsFilterInput.from_dict(data)

                return not_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                not_type_2 = OrNodeLogRecordsFilterInput.from_dict(data)

                return not_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            not_type_3 = NotNodeLogRecordsFilterInput.from_dict(data)

            return not_type_3

        not_ = _parse_not_(d.pop("not"))

        not_node_log_records_filter_input = cls(not_=not_)

        not_node_log_records_filter_input.additional_properties = d
        return not_node_log_records_filter_input

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
