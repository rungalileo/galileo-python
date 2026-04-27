from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.session_notes_response_session_id_to_session_notes import SessionNotesResponseSessionIdToSessionNotes


T = TypeVar("T", bound="SessionNotesResponse")


@_attrs_define
class SessionNotesResponse:
    """
    Attributes:
        session_id_to_session_notes (SessionNotesResponseSessionIdToSessionNotes):
    """

    session_id_to_session_notes: SessionNotesResponseSessionIdToSessionNotes
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        session_id_to_session_notes = self.session_id_to_session_notes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"session_id_to_session_notes": session_id_to_session_notes})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.session_notes_response_session_id_to_session_notes import (
            SessionNotesResponseSessionIdToSessionNotes,
        )

        d = dict(src_dict)
        session_id_to_session_notes = SessionNotesResponseSessionIdToSessionNotes.from_dict(
            d.pop("session_id_to_session_notes")
        )

        session_notes_response = cls(session_id_to_session_notes=session_id_to_session_notes)

        session_notes_response.additional_properties = d
        return session_notes_response

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
