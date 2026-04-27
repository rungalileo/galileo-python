from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.logstream_insight_config import LogstreamInsightConfig


T = TypeVar("T", bound="RunInsightsSettingsSchema")


@_attrs_define
class RunInsightsSettingsSchema:
    """
    Attributes:
        logstream (LogstreamInsightConfig | Unset):
    """

    logstream: LogstreamInsightConfig | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        logstream: dict[str, Any] | Unset = UNSET
        if not isinstance(self.logstream, Unset):
            logstream = self.logstream.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if logstream is not UNSET:
            field_dict["logstream"] = logstream

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.logstream_insight_config import LogstreamInsightConfig

        d = dict(src_dict)
        _logstream = d.pop("logstream", UNSET)
        logstream: LogstreamInsightConfig | Unset
        if isinstance(_logstream, Unset):
            logstream = UNSET
        else:
            logstream = LogstreamInsightConfig.from_dict(_logstream)

        run_insights_settings_schema = cls(logstream=logstream)

        run_insights_settings_schema.additional_properties = d
        return run_insights_settings_schema

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
