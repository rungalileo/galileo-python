from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.like_dislike_constraints import LikeDislikeConstraints
    from ..models.score_constraints import ScoreConstraints
    from ..models.star_constraints import StarConstraints
    from ..models.tags_constraints import TagsConstraints
    from ..models.text_constraints import TextConstraints


T = TypeVar("T", bound="AnnotationTemplateDB")


@_attrs_define
class AnnotationTemplateDB:
    """
    Attributes:
        name (str):
        include_explanation (bool):
        constraints (LikeDislikeConstraints | ScoreConstraints | StarConstraints | TagsConstraints | TextConstraints):
        id (str):
        created_at (datetime.datetime):
        created_by (None | str):
        position (int):
        usage_count (int): Number of annotation ratings using the template.
        criteria (None | str | Unset):
    """

    name: str
    include_explanation: bool
    constraints: LikeDislikeConstraints | ScoreConstraints | StarConstraints | TagsConstraints | TextConstraints
    id: str
    created_at: datetime.datetime
    created_by: None | str
    position: int
    usage_count: int
    criteria: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.like_dislike_constraints import LikeDislikeConstraints
        from ..models.score_constraints import ScoreConstraints
        from ..models.star_constraints import StarConstraints
        from ..models.tags_constraints import TagsConstraints

        name = self.name

        include_explanation = self.include_explanation

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

        id = self.id

        created_at = self.created_at.isoformat()

        created_by: None | str
        created_by = self.created_by

        position = self.position

        usage_count = self.usage_count

        criteria: None | str | Unset
        if isinstance(self.criteria, Unset):
            criteria = UNSET
        else:
            criteria = self.criteria

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "include_explanation": include_explanation,
                "constraints": constraints,
                "id": id,
                "created_at": created_at,
                "created_by": created_by,
                "position": position,
                "usage_count": usage_count,
            }
        )
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

        include_explanation = d.pop("include_explanation")

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

        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        def _parse_created_by(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        created_by = _parse_created_by(d.pop("created_by"))

        position = d.pop("position")

        usage_count = d.pop("usage_count")

        def _parse_criteria(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        criteria = _parse_criteria(d.pop("criteria", UNSET))

        annotation_template_db = cls(
            name=name,
            include_explanation=include_explanation,
            constraints=constraints,
            id=id,
            created_at=created_at,
            created_by=created_by,
            position=position,
            usage_count=usage_count,
            criteria=criteria,
        )

        annotation_template_db.additional_properties = d
        return annotation_template_db

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
