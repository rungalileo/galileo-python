from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AnnotationLikeDislikeAggregate")


@_attrs_define
class AnnotationLikeDislikeAggregate:
    """
    Attributes
    ----------
        like_count (int):
        dislike_count (int):
        unrated_count (int):
        annotation_type (Union[Literal['like_dislike'], Unset]):  Default: 'like_dislike'.
    """

    like_count: int
    dislike_count: int
    unrated_count: int
    annotation_type: Union[Literal["like_dislike"], Unset] = "like_dislike"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        like_count = self.like_count

        dislike_count = self.dislike_count

        unrated_count = self.unrated_count

        annotation_type = self.annotation_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"like_count": like_count, "dislike_count": dislike_count, "unrated_count": unrated_count})
        if annotation_type is not UNSET:
            field_dict["annotation_type"] = annotation_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        like_count = d.pop("like_count")

        dislike_count = d.pop("dislike_count")

        unrated_count = d.pop("unrated_count")

        annotation_type = cast(Union[Literal["like_dislike"], Unset], d.pop("annotation_type", UNSET))
        if annotation_type != "like_dislike" and not isinstance(annotation_type, Unset):
            raise ValueError(f"annotation_type must match const 'like_dislike', got '{annotation_type}'")

        annotation_like_dislike_aggregate = cls(
            like_count=like_count,
            dislike_count=dislike_count,
            unrated_count=unrated_count,
            annotation_type=annotation_type,
        )

        annotation_like_dislike_aggregate.additional_properties = d
        return annotation_like_dislike_aggregate

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
