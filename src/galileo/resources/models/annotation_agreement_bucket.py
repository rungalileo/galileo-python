from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AnnotationAgreementBucket")


@_attrs_define
class AnnotationAgreementBucket:
    """
    Attributes
    ----------
        min_inclusive (float):
        max_exclusive (Union[None, float]):
        count (int):
    """

    min_inclusive: float
    max_exclusive: None | float
    count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        min_inclusive = self.min_inclusive

        max_exclusive: None | float
        max_exclusive = self.max_exclusive

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"min_inclusive": min_inclusive, "max_exclusive": max_exclusive, "count": count})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        min_inclusive = d.pop("min_inclusive")

        def _parse_max_exclusive(data: object) -> None | float:
            if data is None:
                return data
            return cast(None | float, data)

        max_exclusive = _parse_max_exclusive(d.pop("max_exclusive"))

        count = d.pop("count")

        annotation_agreement_bucket = cls(min_inclusive=min_inclusive, max_exclusive=max_exclusive, count=count)

        annotation_agreement_bucket.additional_properties = d
        return annotation_agreement_bucket

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
