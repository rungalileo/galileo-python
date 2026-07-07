import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.choice_rating import ChoiceRating
    from ..models.like_dislike_rating import LikeDislikeRating
    from ..models.score_rating import ScoreRating
    from ..models.star_rating import StarRating
    from ..models.tags_rating import TagsRating
    from ..models.text_rating import TextRating
    from ..models.tree_choice_rating import TreeChoiceRating


T = TypeVar("T", bound="AnnotationRatingDB")


@_attrs_define
class AnnotationRatingDB:
    """
    Attributes:
        rating (Union['ChoiceRating', 'LikeDislikeRating', 'ScoreRating', 'StarRating', 'TagsRating', 'TextRating',
            'TreeChoiceRating']):
        created_at (datetime.datetime):
        created_by (Union[None, str]):
        explanation (Union[None, Unset, str]):
    """

    rating: Union[
        "ChoiceRating", "LikeDislikeRating", "ScoreRating", "StarRating", "TagsRating", "TextRating", "TreeChoiceRating"
    ]
    created_at: datetime.datetime
    created_by: Union[None, str]
    explanation: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.choice_rating import ChoiceRating
        from ..models.like_dislike_rating import LikeDislikeRating
        from ..models.score_rating import ScoreRating
        from ..models.star_rating import StarRating
        from ..models.tags_rating import TagsRating
        from ..models.text_rating import TextRating

        rating: dict[str, Any]
        if isinstance(self.rating, LikeDislikeRating):
            rating = self.rating.to_dict()
        elif isinstance(self.rating, StarRating):
            rating = self.rating.to_dict()
        elif isinstance(self.rating, ScoreRating):
            rating = self.rating.to_dict()
        elif isinstance(self.rating, TagsRating):
            rating = self.rating.to_dict()
        elif isinstance(self.rating, TextRating):
            rating = self.rating.to_dict()
        elif isinstance(self.rating, ChoiceRating):
            rating = self.rating.to_dict()
        else:
            rating = self.rating.to_dict()

        created_at = self.created_at.isoformat()

        created_by: Union[None, str]
        created_by = self.created_by

        explanation: Union[None, Unset, str]
        if isinstance(self.explanation, Unset):
            explanation = UNSET
        else:
            explanation = self.explanation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"rating": rating, "created_at": created_at, "created_by": created_by})
        if explanation is not UNSET:
            field_dict["explanation"] = explanation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.choice_rating import ChoiceRating
        from ..models.like_dislike_rating import LikeDislikeRating
        from ..models.score_rating import ScoreRating
        from ..models.star_rating import StarRating
        from ..models.tags_rating import TagsRating
        from ..models.text_rating import TextRating
        from ..models.tree_choice_rating import TreeChoiceRating

        d = dict(src_dict)

        def _parse_rating(
            data: object,
        ) -> Union[
            "ChoiceRating",
            "LikeDislikeRating",
            "ScoreRating",
            "StarRating",
            "TagsRating",
            "TextRating",
            "TreeChoiceRating",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                rating_type_0 = LikeDislikeRating.from_dict(data)

                return rating_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                rating_type_1 = StarRating.from_dict(data)

                return rating_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                rating_type_2 = ScoreRating.from_dict(data)

                return rating_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                rating_type_3 = TagsRating.from_dict(data)

                return rating_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                rating_type_4 = TextRating.from_dict(data)

                return rating_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                rating_type_5 = ChoiceRating.from_dict(data)

                return rating_type_5
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            rating_type_6 = TreeChoiceRating.from_dict(data)

            return rating_type_6

        rating = _parse_rating(d.pop("rating"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_created_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by = _parse_created_by(d.pop("created_by"))

        def _parse_explanation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        annotation_rating_db = cls(rating=rating, created_at=created_at, created_by=created_by, explanation=explanation)

        annotation_rating_db.additional_properties = d
        return annotation_rating_db

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
