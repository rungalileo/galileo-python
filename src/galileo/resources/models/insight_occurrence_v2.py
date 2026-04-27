from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.span_involved import SpanInvolved


T = TypeVar("T", bound="InsightOccurrenceV2")


@_attrs_define
class InsightOccurrenceV2:
    """
    Attributes:
        session_id (str):
        spans_involved (list[SpanInvolved]):
        session_created_at (datetime.datetime | None | Unset):
    """

    session_id: str
    spans_involved: list[SpanInvolved]
    session_created_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        spans_involved = []
        for spans_involved_item_data in self.spans_involved:
            spans_involved_item = spans_involved_item_data.to_dict()
            spans_involved.append(spans_involved_item)

        session_created_at: None | str | Unset
        if isinstance(self.session_created_at, Unset):
            session_created_at = UNSET
        elif isinstance(self.session_created_at, datetime.datetime):
            session_created_at = self.session_created_at.isoformat()
        else:
            session_created_at = self.session_created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"session_id": session_id, "spans_involved": spans_involved})
        if session_created_at is not UNSET:
            field_dict["session_created_at"] = session_created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.span_involved import SpanInvolved

        d = dict(src_dict)
        session_id = d.pop("session_id")

        spans_involved = []
        _spans_involved = d.pop("spans_involved")
        for spans_involved_item_data in _spans_involved:
            spans_involved_item = SpanInvolved.from_dict(spans_involved_item_data)

            spans_involved.append(spans_involved_item)

        def _parse_session_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                session_created_at_type_0 = isoparse(data)

                return session_created_at_type_0
            except:  # noqa: E722
                pass
            return cast(datetime.datetime | None | Unset, data)

        session_created_at = _parse_session_created_at(d.pop("session_created_at", UNSET))

        insight_occurrence_v2 = cls(
            session_id=session_id, spans_involved=spans_involved, session_created_at=session_created_at
        )

        insight_occurrence_v2.additional_properties = d
        return insight_occurrence_v2

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
