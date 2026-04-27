from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_insights_settings_schema import RunInsightsSettingsSchema


T = TypeVar("T", bound="RunInsightsRequest")


@_attrs_define
class RunInsightsRequest:
    """
    Attributes:
        insights (RunInsightsSettingsSchema | Unset):
    """

    insights: RunInsightsSettingsSchema | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        insights: dict[str, Any] | Unset = UNSET
        if not isinstance(self.insights, Unset):
            insights = self.insights.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if insights is not UNSET:
            field_dict["insights"] = insights

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_insights_settings_schema import RunInsightsSettingsSchema

        d = dict(src_dict)
        _insights = d.pop("insights", UNSET)
        insights: RunInsightsSettingsSchema | Unset
        if isinstance(_insights, Unset):
            insights = UNSET
        else:
            insights = RunInsightsSettingsSchema.from_dict(_insights)

        run_insights_request = cls(insights=insights)

        run_insights_request.additional_properties = d
        return run_insights_request

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
