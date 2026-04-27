from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.insight_db import InsightDB
    from ..models.insight_dbv2 import InsightDBV2


T = TypeVar("T", bound="LogstreamInsightsCreateOrUpdate")


@_attrs_define
class LogstreamInsightsCreateOrUpdate:
    """
    Attributes:
        insights (list[InsightDB] | list[InsightDBV2]):
    """

    insights: list[InsightDB] | list[InsightDBV2]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        insights: list[dict[str, Any]]
        if isinstance(self.insights, list):
            insights = []
            for insights_type_0_item_data in self.insights:
                insights_type_0_item = insights_type_0_item_data.to_dict()
                insights.append(insights_type_0_item)

        else:
            insights = []
            for insights_type_1_item_data in self.insights:
                insights_type_1_item = insights_type_1_item_data.to_dict()
                insights.append(insights_type_1_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"insights": insights})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.insight_db import InsightDB
        from ..models.insight_dbv2 import InsightDBV2

        d = dict(src_dict)

        def _parse_insights(data: object) -> list[InsightDB] | list[InsightDBV2]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                insights_type_0 = []
                _insights_type_0 = data
                for insights_type_0_item_data in _insights_type_0:
                    insights_type_0_item = InsightDBV2.from_dict(insights_type_0_item_data)

                    insights_type_0.append(insights_type_0_item)

                return insights_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            insights_type_1 = []
            _insights_type_1 = data
            for insights_type_1_item_data in _insights_type_1:
                insights_type_1_item = InsightDB.from_dict(insights_type_1_item_data)

                insights_type_1.append(insights_type_1_item)

            return insights_type_1

        insights = _parse_insights(d.pop("insights"))

        logstream_insights_create_or_update = cls(insights=insights)

        logstream_insights_create_or_update.additional_properties = d
        return logstream_insights_create_or_update

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
