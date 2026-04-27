from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.session_titles_response_session_id_to_session_title_type_0 import (
        SessionTitlesResponseSessionIdToSessionTitleType0,
    )


T = TypeVar("T", bound="SessionTitlesResponse")


@_attrs_define
class SessionTitlesResponse:
    """
    Attributes:
        session_id_to_session_title (None | SessionTitlesResponseSessionIdToSessionTitleType0 | Unset):
    """

    session_id_to_session_title: None | SessionTitlesResponseSessionIdToSessionTitleType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.session_titles_response_session_id_to_session_title_type_0 import (
            SessionTitlesResponseSessionIdToSessionTitleType0,
        )

        session_id_to_session_title: dict[str, Any] | None | Unset
        if isinstance(self.session_id_to_session_title, Unset):
            session_id_to_session_title = UNSET
        elif isinstance(self.session_id_to_session_title, SessionTitlesResponseSessionIdToSessionTitleType0):
            session_id_to_session_title = self.session_id_to_session_title.to_dict()
        else:
            session_id_to_session_title = self.session_id_to_session_title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if session_id_to_session_title is not UNSET:
            field_dict["session_id_to_session_title"] = session_id_to_session_title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.session_titles_response_session_id_to_session_title_type_0 import (
            SessionTitlesResponseSessionIdToSessionTitleType0,
        )

        d = dict(src_dict)

        def _parse_session_id_to_session_title(
            data: object,
        ) -> None | SessionTitlesResponseSessionIdToSessionTitleType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                session_id_to_session_title_type_0 = SessionTitlesResponseSessionIdToSessionTitleType0.from_dict(data)

                return session_id_to_session_title_type_0
            except:  # noqa: E722
                pass
            return cast(None | SessionTitlesResponseSessionIdToSessionTitleType0 | Unset, data)

        session_id_to_session_title = _parse_session_id_to_session_title(d.pop("session_id_to_session_title", UNSET))

        session_titles_response = cls(session_id_to_session_title=session_id_to_session_title)

        session_titles_response.additional_properties = d
        return session_titles_response

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
