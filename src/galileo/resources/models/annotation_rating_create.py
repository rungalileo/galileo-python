from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.choice_rating import ChoiceRating
    from ..models.like_dislike_rating import LikeDislikeRating
    from ..models.score_rating import ScoreRating
    from ..models.star_rating import StarRating
    from ..models.tags_rating import TagsRating
    from ..models.text_rating import TextRating
    from ..models.tree_choice_rating import TreeChoiceRating


T = TypeVar("T", bound="AnnotationRatingCreate")


@_attrs_define
class AnnotationRatingCreate:
    """
    Attributes
    ----------
        rating (Union['ChoiceRating', 'LikeDislikeRating', 'ScoreRating', 'StarRating', 'TagsRating', 'TextRating',
            'TreeChoiceRating']):
        explanation (Union[None, Unset, str]):
    """

    rating: Union[
        "ChoiceRating", "LikeDislikeRating", "ScoreRating", "StarRating", "TagsRating", "TextRating", "TreeChoiceRating"
    ]
    explanation: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.choice_rating import ChoiceRating
        from ..models.like_dislike_rating import LikeDislikeRating
        from ..models.score_rating import ScoreRating
        from ..models.star_rating import StarRating
        from ..models.tags_rating import TagsRating
        from ..models.text_rating import TextRating

        rating: dict[str, Any]
        if isinstance(
            self.rating, LikeDislikeRating | StarRating | ScoreRating | TagsRating | (TextRating | ChoiceRating)
        ):
            rating = self.rating.to_dict()
        else:
            rating = self.rating.to_dict()

        explanation: None | Unset | str
        explanation = UNSET if isinstance(self.explanation, Unset) else self.explanation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"rating": rating})
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
                return LikeDislikeRating.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return StarRating.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ScoreRating.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return TagsRating.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return TextRating.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ChoiceRating.from_dict(data)

            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            return TreeChoiceRating.from_dict(data)

        rating = _parse_rating(d.pop("rating"))

        def _parse_explanation(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        annotation_rating_create = cls(rating=rating, explanation=explanation)

        annotation_rating_create.additional_properties = d
        return annotation_rating_create

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
