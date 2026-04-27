from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FeedbackCountsRequest")


@_attrs_define
class FeedbackCountsRequest:
    """Request schema for querying feedback counts by scorer IDs.

    Attributes:
        scorer_ids (list[str]): List of scorer IDs to query feedback counts for
    """

    scorer_ids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scorer_ids = self.scorer_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"scorer_ids": scorer_ids})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scorer_ids = cast(list[str], d.pop("scorer_ids"))

        feedback_counts_request = cls(scorer_ids=scorer_ids)

        feedback_counts_request.additional_properties = d
        return feedback_counts_request

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
