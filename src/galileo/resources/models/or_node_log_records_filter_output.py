from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.and_node_log_records_filter_output import AndNodeLogRecordsFilterOutput
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.not_node_log_records_filter_output import NotNodeLogRecordsFilterOutput


T = TypeVar("T", bound="OrNodeLogRecordsFilterOutput")


@_attrs_define
class OrNodeLogRecordsFilterOutput:
    """
    Attributes:
        or_ (list[AndNodeLogRecordsFilterOutput | FilterLeafLogRecordsFilter | NotNodeLogRecordsFilterOutput |
            OrNodeLogRecordsFilterOutput]):
    """

    or_: list[
        AndNodeLogRecordsFilterOutput
        | FilterLeafLogRecordsFilter
        | NotNodeLogRecordsFilterOutput
        | OrNodeLogRecordsFilterOutput
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node_log_records_filter_output import AndNodeLogRecordsFilterOutput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter

        or_ = []
        for or_item_data in self.or_:
            or_item: dict[str, Any]
            if isinstance(or_item_data, FilterLeafLogRecordsFilter):
                or_item = or_item_data.to_dict()
            elif isinstance(or_item_data, AndNodeLogRecordsFilterOutput):
                or_item = or_item_data.to_dict()
            elif isinstance(or_item_data, OrNodeLogRecordsFilterOutput):
                or_item = or_item_data.to_dict()
            else:
                or_item = or_item_data.to_dict()

            or_.append(or_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"or": or_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node_log_records_filter_output import AndNodeLogRecordsFilterOutput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.not_node_log_records_filter_output import NotNodeLogRecordsFilterOutput

        d = dict(src_dict)
        or_ = []
        _or_ = d.pop("or")
        for or_item_data in _or_:

            def _parse_or_item(
                data: object,
            ) -> (
                AndNodeLogRecordsFilterOutput
                | FilterLeafLogRecordsFilter
                | NotNodeLogRecordsFilterOutput
                | OrNodeLogRecordsFilterOutput
            ):
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    or_item_type_0 = FilterLeafLogRecordsFilter.from_dict(data)

                    return or_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    or_item_type_1 = AndNodeLogRecordsFilterOutput.from_dict(data)

                    return or_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    or_item_type_2 = OrNodeLogRecordsFilterOutput.from_dict(data)

                    return or_item_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                or_item_type_3 = NotNodeLogRecordsFilterOutput.from_dict(data)

                return or_item_type_3

            or_item = _parse_or_item(or_item_data)

            or_.append(or_item)

        or_node_log_records_filter_output = cls(or_=or_)

        or_node_log_records_filter_output.additional_properties = d
        return or_node_log_records_filter_output

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
