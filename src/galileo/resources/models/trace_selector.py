from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TraceSelector")


@_attrs_define
class TraceSelector:
    """Choose specific traces to apply the bulk operation to.

    Attributes:
        traces (list[str]):
        selector_type (Literal['traces'] | Unset):  Default: 'traces'.
    """

    traces: list[str]
    selector_type: Literal["traces"] | Unset = "traces"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        traces = self.traces

        selector_type = self.selector_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"traces": traces})
        if selector_type is not UNSET:
            field_dict["selector_type"] = selector_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        traces = cast(list[str], d.pop("traces"))

        selector_type = cast(Literal["traces"] | Unset, d.pop("selector_type", UNSET))
        if selector_type != "traces" and not isinstance(selector_type, Unset):
            raise ValueError(f"selector_type must match const 'traces', got '{selector_type}'")

        trace_selector = cls(traces=traces, selector_type=selector_type)

        trace_selector.additional_properties = d
        return trace_selector

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
