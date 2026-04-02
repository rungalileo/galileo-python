from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AnnotationTextAggregate")


@_attrs_define
class AnnotationTextAggregate:
    """
    Attributes
    ----------
        count (int):
        unrated_count (int):
        annotation_type (Union[Literal['text'], Unset]):  Default: 'text'.
    """

    count: int
    unrated_count: int
    annotation_type: Union[Literal["text"], Unset] = "text"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        unrated_count = self.unrated_count

        annotation_type = self.annotation_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"count": count, "unrated_count": unrated_count})
        if annotation_type is not UNSET:
            field_dict["annotation_type"] = annotation_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        unrated_count = d.pop("unrated_count")

        annotation_type = cast(Union[Literal["text"], Unset], d.pop("annotation_type", UNSET))
        if annotation_type != "text" and not isinstance(annotation_type, Unset):
            raise ValueError(f"annotation_type must match const 'text', got '{annotation_type}'")

        annotation_text_aggregate = cls(count=count, unrated_count=unrated_count, annotation_type=annotation_type)

        annotation_text_aggregate.additional_properties = d
        return annotation_text_aggregate

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
