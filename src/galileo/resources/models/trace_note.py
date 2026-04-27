from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.span_note import SpanNote


T = TypeVar("T", bound="TraceNote")


@_attrs_define
class TraceNote:
    """
    Attributes:
        note_text (str):
        spans_involved (list[SpanNote]):
    """

    note_text: str
    spans_involved: list[SpanNote]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        note_text = self.note_text

        spans_involved = []
        for spans_involved_item_data in self.spans_involved:
            spans_involved_item = spans_involved_item_data.to_dict()
            spans_involved.append(spans_involved_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"note_text": note_text, "spans_involved": spans_involved})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span_note import SpanNote

        d = dict(src_dict)
        note_text = d.pop("note_text")

        spans_involved = []
        _spans_involved = d.pop("spans_involved")
        for spans_involved_item_data in _spans_involved:
            spans_involved_item = SpanNote.from_dict(spans_involved_item_data)

            spans_involved.append(spans_involved_item)

        trace_note = cls(note_text=note_text, spans_involved=spans_involved)

        trace_note.additional_properties = d
        return trace_note

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
