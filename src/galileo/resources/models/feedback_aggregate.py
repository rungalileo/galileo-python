from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.like_dislike_aggregate import LikeDislikeAggregate
    from ..models.score_aggregate import ScoreAggregate
    from ..models.star_aggregate import StarAggregate
    from ..models.tags_aggregate import TagsAggregate


T = TypeVar("T", bound="FeedbackAggregate")


@_attrs_define
class FeedbackAggregate:
    """
    Attributes:
        aggregate (Union['LikeDislikeAggregate', 'ScoreAggregate', 'StarAggregate', 'TagsAggregate']):
    """

    aggregate: Union["LikeDislikeAggregate", "ScoreAggregate", "StarAggregate", "TagsAggregate"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.like_dislike_aggregate import LikeDislikeAggregate
        from ..models.score_aggregate import ScoreAggregate
        from ..models.star_aggregate import StarAggregate

        aggregate: dict[str, Any]
        if isinstance(self.aggregate, LikeDislikeAggregate):
            aggregate = self.aggregate.to_dict()
        elif isinstance(self.aggregate, StarAggregate):
            aggregate = self.aggregate.to_dict()
        elif isinstance(self.aggregate, ScoreAggregate):
            aggregate = self.aggregate.to_dict()
        else:
            aggregate = self.aggregate.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"aggregate": aggregate})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.like_dislike_aggregate import LikeDislikeAggregate
        from ..models.score_aggregate import ScoreAggregate
        from ..models.star_aggregate import StarAggregate
        from ..models.tags_aggregate import TagsAggregate

        d = src_dict.copy()

        def _parse_aggregate(
            data: object,
        ) -> Union["LikeDislikeAggregate", "ScoreAggregate", "StarAggregate", "TagsAggregate"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregate_type_0 = LikeDislikeAggregate.from_dict(data)

                return aggregate_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregate_type_1 = StarAggregate.from_dict(data)

                return aggregate_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregate_type_2 = ScoreAggregate.from_dict(data)

                return aggregate_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            aggregate_type_3 = TagsAggregate.from_dict(data)

            return aggregate_type_3

        aggregate = _parse_aggregate(d.pop("aggregate"))

        feedback_aggregate = cls(aggregate=aggregate)

        feedback_aggregate.additional_properties = d
        return feedback_aggregate

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
