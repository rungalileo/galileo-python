from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.like_dislike_constraints import LikeDislikeConstraints
    from ..models.score_constraints import ScoreConstraints
    from ..models.star_constraints import StarConstraints
    from ..models.tags_constraints import TagsConstraints
    from ..models.text_constraints import TextConstraints


T = TypeVar("T", bound="AnnotationTemplateCreate")


@_attrs_define
class AnnotationTemplateCreate:
    """
    Attributes:
        name (str):
        constraints (LikeDislikeConstraints | ScoreConstraints | StarConstraints | TagsConstraints | TextConstraints):
        include_explanation (bool | Unset):  Default: False.
        criteria (None | str | Unset):
    """

    name: str
    constraints: LikeDislikeConstraints | ScoreConstraints | StarConstraints | TagsConstraints | TextConstraints
    include_explanation: bool | Unset = False
    criteria: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.like_dislike_constraints import LikeDislikeConstraints
        from ..models.score_constraints import ScoreConstraints
        from ..models.star_constraints import StarConstraints
        from ..models.tags_constraints import TagsConstraints

        name = self.name

        constraints: dict[str, Any]
        if isinstance(self.constraints, LikeDislikeConstraints):
            constraints = self.constraints.to_dict()
        elif isinstance(self.constraints, StarConstraints):
            constraints = self.constraints.to_dict()
        elif isinstance(self.constraints, ScoreConstraints):
            constraints = self.constraints.to_dict()
        elif isinstance(self.constraints, TagsConstraints):
            constraints = self.constraints.to_dict()
        else:
            constraints = self.constraints.to_dict()

        include_explanation = self.include_explanation

        criteria: None | str | Unset
        if isinstance(self.criteria, Unset):
            criteria = UNSET
        else:
            criteria = self.criteria

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
        from ..models.like_dislike_constraints import LikeDislikeConstraints
        from ..models.score_constraints import ScoreConstraints
        from ..models.star_constraints import StarConstraints
        from ..models.tags_constraints import TagsConstraints
        from ..models.text_constraints import TextConstraints

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_constraints(
            data: object,
        ) -> LikeDislikeConstraints | ScoreConstraints | StarConstraints | TagsConstraints | TextConstraints:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                constraints_type_0 = LikeDislikeConstraints.from_dict(data)

                return constraints_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                constraints_type_1 = StarConstraints.from_dict(data)

                return constraints_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                constraints_type_2 = ScoreConstraints.from_dict(data)

                return constraints_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                constraints_type_3 = TagsConstraints.from_dict(data)

                return constraints_type_3
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            constraints_type_4 = TextConstraints.from_dict(data)

            return constraints_type_4

        constraints = _parse_constraints(d.pop("constraints"))

        include_explanation = d.pop("include_explanation", UNSET)

        def _parse_criteria(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

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
