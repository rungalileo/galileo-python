from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.choice_constraints import ChoiceConstraints
    from ..models.like_dislike_constraints import LikeDislikeConstraints
    from ..models.score_constraints import ScoreConstraints
    from ..models.star_constraints import StarConstraints
    from ..models.tags_constraints import TagsConstraints
    from ..models.text_constraints import TextConstraints
    from ..models.tree_choice_constraints import TreeChoiceConstraints


T = TypeVar("T", bound="AnnotationTemplateCreate")


@_attrs_define
class AnnotationTemplateCreate:
    """
    Attributes
    ----------
        name (str):
        constraints (Union['ChoiceConstraints', 'LikeDislikeConstraints', 'ScoreConstraints', 'StarConstraints',
            'TagsConstraints', 'TextConstraints', 'TreeChoiceConstraints']):
        include_explanation (Union[Unset, bool]):  Default: False.
        criteria (Union[None, Unset, str]):
    """

    name: str
    constraints: Union[
        "ChoiceConstraints",
        "LikeDislikeConstraints",
        "ScoreConstraints",
        "StarConstraints",
        "TagsConstraints",
        "TextConstraints",
        "TreeChoiceConstraints",
    ]
    include_explanation: Unset | bool = False
    criteria: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.choice_constraints import ChoiceConstraints
        from ..models.like_dislike_constraints import LikeDislikeConstraints
        from ..models.score_constraints import ScoreConstraints
        from ..models.star_constraints import StarConstraints
        from ..models.tags_constraints import TagsConstraints
        from ..models.text_constraints import TextConstraints

        name = self.name

        constraints: dict[str, Any]
        if isinstance(
            self.constraints,
            LikeDislikeConstraints
            | StarConstraints
            | ScoreConstraints
            | TagsConstraints
            | (TextConstraints | ChoiceConstraints),
        ):
            constraints = self.constraints.to_dict()
        else:
            constraints = self.constraints.to_dict()

        include_explanation = self.include_explanation

        criteria: None | Unset | str
        criteria = UNSET if isinstance(self.criteria, Unset) else self.criteria

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "constraints": constraints})
        if include_explanation is not UNSET:
            field_dict["include_explanation"] = include_explanation
        if criteria is not UNSET:
            field_dict["criteria"] = criteria

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.choice_constraints import ChoiceConstraints
        from ..models.like_dislike_constraints import LikeDislikeConstraints
        from ..models.score_constraints import ScoreConstraints
        from ..models.star_constraints import StarConstraints
        from ..models.tags_constraints import TagsConstraints
        from ..models.text_constraints import TextConstraints
        from ..models.tree_choice_constraints import TreeChoiceConstraints

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_constraints(
            data: object,
        ) -> Union[
            "ChoiceConstraints",
            "LikeDislikeConstraints",
            "ScoreConstraints",
            "StarConstraints",
            "TagsConstraints",
            "TextConstraints",
            "TreeChoiceConstraints",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return LikeDislikeConstraints.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return StarConstraints.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ScoreConstraints.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return TagsConstraints.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return TextConstraints.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ChoiceConstraints.from_dict(data)

            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            return TreeChoiceConstraints.from_dict(data)

        constraints = _parse_constraints(d.pop("constraints"))

        include_explanation = d.pop("include_explanation", UNSET)

        def _parse_criteria(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        criteria = _parse_criteria(d.pop("criteria", UNSET))

        annotation_template_create = cls(
            name=name, constraints=constraints, include_explanation=include_explanation, criteria=criteria
        )

        annotation_template_create.additional_properties = d
        return annotation_template_create

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
