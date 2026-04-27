from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.feedback_counts_response_feedback_counts import FeedbackCountsResponseFeedbackCounts


T = TypeVar("T", bound="FeedbackCountsResponse")


@_attrs_define
class FeedbackCountsResponse:
    """Response schema mapping scorer IDs to their active queue feedback counts.

    Attributes:
        feedback_counts (FeedbackCountsResponseFeedbackCounts): Map of scorer_id to count of feedback items in the
            scorer's active queue. Returns 0 for scorers with no active queue.
    """

    feedback_counts: FeedbackCountsResponseFeedbackCounts
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feedback_counts = self.feedback_counts.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"feedback_counts": feedback_counts})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.feedback_counts_response_feedback_counts import FeedbackCountsResponseFeedbackCounts

        d = dict(src_dict)
        feedback_counts = FeedbackCountsResponseFeedbackCounts.from_dict(d.pop("feedback_counts"))

        feedback_counts_response = cls(feedback_counts=feedback_counts)

        feedback_counts_response.additional_properties = d
        return feedback_counts_response

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
