from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LikeDislikeAggregate")


@_attrs_define
class LikeDislikeAggregate:
    """
    Attributes:
        dislike_count (int):
        like_count (int):
        unrated_count (int):
        feedback_type (Union[Literal['like_dislike'], Unset]):  Default: 'like_dislike'.
    """

    dislike_count: int
    like_count: int
    unrated_count: int
    feedback_type: Union[Literal["like_dislike"], Unset] = "like_dislike"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dislike_count = self.dislike_count

        like_count = self.like_count

        unrated_count = self.unrated_count

        feedback_type = self.feedback_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"dislike_count": dislike_count, "like_count": like_count, "unrated_count": unrated_count})
        if feedback_type is not UNSET:
            field_dict["feedback_type"] = feedback_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        dislike_count = d.pop("dislike_count")

        like_count = d.pop("like_count")

        unrated_count = d.pop("unrated_count")

        feedback_type = cast(Union[Literal["like_dislike"], Unset], d.pop("feedback_type", UNSET))
        if feedback_type != "like_dislike" and not isinstance(feedback_type, Unset):
            raise ValueError(f"feedback_type must match const 'like_dislike', got '{feedback_type}'")

        like_dislike_aggregate = cls(
            dislike_count=dislike_count, like_count=like_count, unrated_count=unrated_count, feedback_type=feedback_type
        )

        like_dislike_aggregate.additional_properties = d
        return like_dislike_aggregate

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
