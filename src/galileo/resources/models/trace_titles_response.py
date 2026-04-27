from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trace_titles_response_trace_id_to_trace_title_type_0 import (
        TraceTitlesResponseTraceIdToTraceTitleType0,
    )


T = TypeVar("T", bound="TraceTitlesResponse")


@_attrs_define
class TraceTitlesResponse:
    """
    Attributes:
        trace_id_to_trace_title (None | TraceTitlesResponseTraceIdToTraceTitleType0 | Unset):
    """

    trace_id_to_trace_title: None | TraceTitlesResponseTraceIdToTraceTitleType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.trace_titles_response_trace_id_to_trace_title_type_0 import (
            TraceTitlesResponseTraceIdToTraceTitleType0,
        )

        trace_id_to_trace_title: dict[str, Any] | None | Unset
        if isinstance(self.trace_id_to_trace_title, Unset):
            trace_id_to_trace_title = UNSET
        elif isinstance(self.trace_id_to_trace_title, TraceTitlesResponseTraceIdToTraceTitleType0):
            trace_id_to_trace_title = self.trace_id_to_trace_title.to_dict()
        else:
            trace_id_to_trace_title = self.trace_id_to_trace_title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trace_id_to_trace_title is not UNSET:
            field_dict["trace_id_to_trace_title"] = trace_id_to_trace_title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trace_titles_response_trace_id_to_trace_title_type_0 import (
            TraceTitlesResponseTraceIdToTraceTitleType0,
        )

        d = dict(src_dict)

        def _parse_trace_id_to_trace_title(data: object) -> None | TraceTitlesResponseTraceIdToTraceTitleType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                trace_id_to_trace_title_type_0 = TraceTitlesResponseTraceIdToTraceTitleType0.from_dict(data)

                return trace_id_to_trace_title_type_0
            except:  # noqa: E722
                pass
            return cast(None | TraceTitlesResponseTraceIdToTraceTitleType0 | Unset, data)

        trace_id_to_trace_title = _parse_trace_id_to_trace_title(d.pop("trace_id_to_trace_title", UNSET))

        trace_titles_response = cls(trace_id_to_trace_title=trace_id_to_trace_title)

        trace_titles_response.additional_properties = d
        return trace_titles_response

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
