from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.not_node_log_records_filter_output import NotNodeLogRecordsFilterOutput
    from ..models.or_node_log_records_filter_output import OrNodeLogRecordsFilterOutput


T = TypeVar("T", bound="AndNodeLogRecordsFilterOutput")


@_attrs_define
class AndNodeLogRecordsFilterOutput:
    """
    Attributes:
        and_ (list[AndNodeLogRecordsFilterOutput | FilterLeafLogRecordsFilter | NotNodeLogRecordsFilterOutput |
            OrNodeLogRecordsFilterOutput]):
    """

    and_: list[
        AndNodeLogRecordsFilterOutput
        | FilterLeafLogRecordsFilter
        | NotNodeLogRecordsFilterOutput
        | OrNodeLogRecordsFilterOutput
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.or_node_log_records_filter_output import OrNodeLogRecordsFilterOutput

        and_ = []
        for and_item_data in self.and_:
            and_item: dict[str, Any]
            if isinstance(and_item_data, FilterLeafLogRecordsFilter):
                and_item = and_item_data.to_dict()
            elif isinstance(and_item_data, AndNodeLogRecordsFilterOutput):
                and_item = and_item_data.to_dict()
            elif isinstance(and_item_data, OrNodeLogRecordsFilterOutput):
                and_item = and_item_data.to_dict()
            else:
                and_item = and_item_data.to_dict()

            and_.append(and_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"and": and_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.not_node_log_records_filter_output import NotNodeLogRecordsFilterOutput
        from ..models.or_node_log_records_filter_output import OrNodeLogRecordsFilterOutput

        d = dict(src_dict)
        and_ = []
        _and_ = d.pop("and")
        for and_item_data in _and_:

            def _parse_and_item(
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
                    and_item_type_0 = FilterLeafLogRecordsFilter.from_dict(data)

                    return and_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    and_item_type_1 = AndNodeLogRecordsFilterOutput.from_dict(data)

                    return and_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    and_item_type_2 = OrNodeLogRecordsFilterOutput.from_dict(data)

                    return and_item_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                and_item_type_3 = NotNodeLogRecordsFilterOutput.from_dict(data)

                return and_item_type_3

            and_item = _parse_and_item(and_item_data)

            and_.append(and_item)

        and_node_log_records_filter_output = cls(and_=and_)

        and_node_log_records_filter_output.additional_properties = d
        return and_node_log_records_filter_output

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
