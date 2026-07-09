from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.annotation_like_dislike_aggregate import AnnotationLikeDislikeAggregate
    from ..models.annotation_score_aggregate import AnnotationScoreAggregate
    from ..models.annotation_star_aggregate import AnnotationStarAggregate
    from ..models.annotation_tags_aggregate import AnnotationTagsAggregate
    from ..models.annotation_text_aggregate import AnnotationTextAggregate


T = TypeVar("T", bound="AnnotationAggregate")


@_attrs_define
class AnnotationAggregate:
    """
    Attributes:
        aggregate (AnnotationLikeDislikeAggregate | AnnotationScoreAggregate | AnnotationStarAggregate |
            AnnotationTagsAggregate | AnnotationTextAggregate):
    """

    aggregate: (
        AnnotationLikeDislikeAggregate
        | AnnotationScoreAggregate
        | AnnotationStarAggregate
        | AnnotationTagsAggregate
        | AnnotationTextAggregate
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.annotation_like_dislike_aggregate import AnnotationLikeDislikeAggregate
        from ..models.annotation_score_aggregate import AnnotationScoreAggregate
        from ..models.annotation_star_aggregate import AnnotationStarAggregate
        from ..models.annotation_tags_aggregate import AnnotationTagsAggregate

        aggregate: dict[str, Any]
        if isinstance(self.aggregate, AnnotationLikeDislikeAggregate):
            aggregate = self.aggregate.to_dict()
        elif isinstance(self.aggregate, AnnotationStarAggregate):
            aggregate = self.aggregate.to_dict()
        elif isinstance(self.aggregate, AnnotationScoreAggregate):
            aggregate = self.aggregate.to_dict()
        elif isinstance(self.aggregate, AnnotationTagsAggregate):
            aggregate = self.aggregate.to_dict()
        else:
            aggregate = self.aggregate.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"aggregate": aggregate})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_like_dislike_aggregate import AnnotationLikeDislikeAggregate
        from ..models.annotation_score_aggregate import AnnotationScoreAggregate
        from ..models.annotation_star_aggregate import AnnotationStarAggregate
        from ..models.annotation_tags_aggregate import AnnotationTagsAggregate
        from ..models.annotation_text_aggregate import AnnotationTextAggregate

        d = dict(src_dict)

        def _parse_aggregate(
            data: object,
        ) -> (
            AnnotationLikeDislikeAggregate
            | AnnotationScoreAggregate
            | AnnotationStarAggregate
            | AnnotationTagsAggregate
            | AnnotationTextAggregate
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregate_type_0 = AnnotationLikeDislikeAggregate.from_dict(data)

                return aggregate_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregate_type_1 = AnnotationStarAggregate.from_dict(data)

                return aggregate_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregate_type_2 = AnnotationScoreAggregate.from_dict(data)

                return aggregate_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregate_type_3 = AnnotationTagsAggregate.from_dict(data)

                return aggregate_type_3
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            aggregate_type_4 = AnnotationTextAggregate.from_dict(data)

            return aggregate_type_4

        aggregate = _parse_aggregate(d.pop("aggregate"))

        annotation_aggregate = cls(aggregate=aggregate)

        annotation_aggregate.additional_properties = d
        return annotation_aggregate

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
