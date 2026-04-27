from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.insight_v2_priority_category_type_0 import InsightV2PriorityCategoryType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.insight_example_occurrence_v2 import InsightExampleOccurrenceV2
    from ..models.insight_occurrence_v2 import InsightOccurrenceV2


T = TypeVar("T", bound="InsightV2")


@_attrs_define
class InsightV2:
    """
    Attributes:
        title (str):
        observation (str):
        details (str):
        suggested_action (str):
        all_occurrences (list[InsightOccurrenceV2]):
        example_occurrences (list[InsightExampleOccurrenceV2]):
        priority (int):
        priority_category (InsightV2PriorityCategoryType0 | None | Unset):
        input_data_latest_updated_ts (datetime.datetime | None | Unset):
    """

    title: str
    observation: str
    details: str
    suggested_action: str
    all_occurrences: list[InsightOccurrenceV2]
    example_occurrences: list[InsightExampleOccurrenceV2]
    priority: int
    priority_category: InsightV2PriorityCategoryType0 | None | Unset = UNSET
    input_data_latest_updated_ts: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        observation = self.observation

        details = self.details

        suggested_action = self.suggested_action

        all_occurrences = []
        for all_occurrences_item_data in self.all_occurrences:
            all_occurrences_item = all_occurrences_item_data.to_dict()
            all_occurrences.append(all_occurrences_item)

        example_occurrences = []
        for example_occurrences_item_data in self.example_occurrences:
            example_occurrences_item = example_occurrences_item_data.to_dict()
            example_occurrences.append(example_occurrences_item)

        priority = self.priority

        priority_category: None | str | Unset
        if isinstance(self.priority_category, Unset):
            priority_category = UNSET
        elif isinstance(self.priority_category, InsightV2PriorityCategoryType0):
            priority_category = self.priority_category.value
        else:
            priority_category = self.priority_category

        input_data_latest_updated_ts: None | str | Unset
        if isinstance(self.input_data_latest_updated_ts, Unset):
            input_data_latest_updated_ts = UNSET
        elif isinstance(self.input_data_latest_updated_ts, datetime.datetime):
            input_data_latest_updated_ts = self.input_data_latest_updated_ts.isoformat()
        else:
            input_data_latest_updated_ts = self.input_data_latest_updated_ts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "observation": observation,
                "details": details,
                "suggested_action": suggested_action,
                "all_occurrences": all_occurrences,
                "example_occurrences": example_occurrences,
                "priority": priority,
            }
        )
        if priority_category is not UNSET:
            field_dict["priority_category"] = priority_category
        if input_data_latest_updated_ts is not UNSET:
            field_dict["input_data_latest_updated_ts"] = input_data_latest_updated_ts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.insight_example_occurrence_v2 import InsightExampleOccurrenceV2
        from ..models.insight_occurrence_v2 import InsightOccurrenceV2

        d = dict(src_dict)
        title = d.pop("title")

        observation = d.pop("observation")

        details = d.pop("details")

        suggested_action = d.pop("suggested_action")

        all_occurrences = []
        _all_occurrences = d.pop("all_occurrences")
        for all_occurrences_item_data in _all_occurrences:
            all_occurrences_item = InsightOccurrenceV2.from_dict(all_occurrences_item_data)

            all_occurrences.append(all_occurrences_item)

        example_occurrences = []
        _example_occurrences = d.pop("example_occurrences")
        for example_occurrences_item_data in _example_occurrences:
            example_occurrences_item = InsightExampleOccurrenceV2.from_dict(example_occurrences_item_data)

            example_occurrences.append(example_occurrences_item)

        priority = d.pop("priority")

        def _parse_priority_category(data: object) -> InsightV2PriorityCategoryType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                priority_category_type_0 = InsightV2PriorityCategoryType0(data)

                return priority_category_type_0
            except:  # noqa: E722
                pass
            return cast(InsightV2PriorityCategoryType0 | None | Unset, data)

        priority_category = _parse_priority_category(d.pop("priority_category", UNSET))

        def _parse_input_data_latest_updated_ts(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                input_data_latest_updated_ts_type_0 = isoparse(data)

                return input_data_latest_updated_ts_type_0
            except:  # noqa: E722
                pass
            return cast(datetime.datetime | None | Unset, data)

        input_data_latest_updated_ts = _parse_input_data_latest_updated_ts(d.pop("input_data_latest_updated_ts", UNSET))

        insight_v2 = cls(
            title=title,
            observation=observation,
            details=details,
            suggested_action=suggested_action,
            all_occurrences=all_occurrences,
            example_occurrences=example_occurrences,
            priority=priority,
            priority_category=priority_category,
            input_data_latest_updated_ts=input_data_latest_updated_ts,
        )

        insight_v2.additional_properties = d
        return insight_v2

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
