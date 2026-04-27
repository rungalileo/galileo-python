from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.trace_notes_response_trace_id_to_trace_notes import TraceNotesResponseTraceIdToTraceNotes


T = TypeVar("T", bound="TraceNotesResponse")


@_attrs_define
class TraceNotesResponse:
    """
    Attributes:
        trace_id_to_trace_notes (TraceNotesResponseTraceIdToTraceNotes):
    """

    trace_id_to_trace_notes: TraceNotesResponseTraceIdToTraceNotes
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trace_id_to_trace_notes = self.trace_id_to_trace_notes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"trace_id_to_trace_notes": trace_id_to_trace_notes})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trace_notes_response_trace_id_to_trace_notes import TraceNotesResponseTraceIdToTraceNotes

        d = dict(src_dict)
        trace_id_to_trace_notes = TraceNotesResponseTraceIdToTraceNotes.from_dict(d.pop("trace_id_to_trace_notes"))

        trace_notes_response = cls(trace_id_to_trace_notes=trace_id_to_trace_notes)

        trace_notes_response.additional_properties = d
        return trace_notes_response

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
