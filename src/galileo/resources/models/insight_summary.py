from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.insight_summary_priority_category_type_0 import InsightSummaryPriorityCategoryType0
from ..types import UNSET, Unset

T = TypeVar("T", bound="InsightSummary")


@_attrs_define
class InsightSummary:
    """
    Attributes
    ----------
        id (str):
        title (str):
        observation (str):
        details (str):
        suggested_action (str):
        priority (int):
        priority_category (Union[InsightSummaryPriorityCategoryType0, None, Unset]):
    """

    id: str
    title: str
    observation: str
    details: str
    suggested_action: str
    priority: int
    priority_category: Union[InsightSummaryPriorityCategoryType0, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        observation = self.observation

        details = self.details

        suggested_action = self.suggested_action

        priority = self.priority

        priority_category: Union[None, Unset, str]
        if isinstance(self.priority_category, Unset):
            priority_category = UNSET
        elif isinstance(self.priority_category, InsightSummaryPriorityCategoryType0):
            priority_category = self.priority_category.value
        else:
            priority_category = self.priority_category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "observation": observation,
                "details": details,
                "suggested_action": suggested_action,
                "priority": priority,
            }
        )
        if priority_category is not UNSET:
            field_dict["priority_category"] = priority_category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        title = d.pop("title")

        observation = d.pop("observation")

        details = d.pop("details")

        suggested_action = d.pop("suggested_action")

        priority = d.pop("priority")

        def _parse_priority_category(data: object) -> Union[InsightSummaryPriorityCategoryType0, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return InsightSummaryPriorityCategoryType0(data)

            except:  # noqa: E722
                pass
            return cast(Union[InsightSummaryPriorityCategoryType0, None, Unset], data)

        priority_category = _parse_priority_category(d.pop("priority_category", UNSET))

        insight_summary = cls(
            id=id,
            title=title,
            observation=observation,
            details=details,
            suggested_action=suggested_action,
            priority=priority,
            priority_category=priority_category,
        )

        insight_summary.additional_properties = d
        return insight_summary

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
