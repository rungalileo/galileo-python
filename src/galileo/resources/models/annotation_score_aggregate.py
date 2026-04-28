from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.score_bucket import ScoreBucket


T = TypeVar("T", bound="AnnotationScoreAggregate")


@_attrs_define
class AnnotationScoreAggregate:
    """
    Attributes
    ----------
        buckets (list[ScoreBucket]):
        average (float):
        unrated_count (int):
        annotation_type (Literal['score'] | Unset):  Default: 'score'.
    """

    buckets: list[ScoreBucket]
    average: float
    unrated_count: int
    annotation_type: Literal["score"] | Unset = "score"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        buckets = []
        for buckets_item_data in self.buckets:
            buckets_item = buckets_item_data.to_dict()
            buckets.append(buckets_item)

        average = self.average

        unrated_count = self.unrated_count

        annotation_type = self.annotation_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"buckets": buckets, "average": average, "unrated_count": unrated_count})
        if annotation_type is not UNSET:
            field_dict["annotation_type"] = annotation_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.score_bucket import ScoreBucket

        d = dict(src_dict)
        buckets = []
        _buckets = d.pop("buckets")
        for buckets_item_data in _buckets:
            buckets_item = ScoreBucket.from_dict(buckets_item_data)

            buckets.append(buckets_item)

        average = d.pop("average")

        unrated_count = d.pop("unrated_count")

        annotation_type = cast(Literal["score"] | Unset, d.pop("annotation_type", UNSET))
        if annotation_type != "score" and not isinstance(annotation_type, Unset):
            raise ValueError(f"annotation_type must match const 'score', got '{annotation_type}'")

        annotation_score_aggregate = cls(
            buckets=buckets, average=average, unrated_count=unrated_count, annotation_type=annotation_type
        )

        annotation_score_aggregate.additional_properties = d
        return annotation_score_aggregate

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
