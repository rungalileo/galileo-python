from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.annotation_agreement_bucket import AnnotationAgreementBucket


T = TypeVar("T", bound="AnnotationAgreementAggregate")


@_attrs_define
class AnnotationAgreementAggregate:
    """
    Attributes:
        buckets (list['AnnotationAgreementBucket']):
        average_agreement (float):
    """

    buckets: list["AnnotationAgreementBucket"]
    average_agreement: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        buckets = []
        for buckets_item_data in self.buckets:
            buckets_item = buckets_item_data.to_dict()
            buckets.append(buckets_item)

        average_agreement = self.average_agreement

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"buckets": buckets, "average_agreement": average_agreement})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_agreement_bucket import AnnotationAgreementBucket

        d = dict(src_dict)
        buckets = []
        _buckets = d.pop("buckets")
        for buckets_item_data in _buckets:
            buckets_item = AnnotationAgreementBucket.from_dict(buckets_item_data)

            buckets.append(buckets_item)

        average_agreement = d.pop("average_agreement")

        annotation_agreement_aggregate = cls(buckets=buckets, average_agreement=average_agreement)

        annotation_agreement_aggregate.additional_properties = d
        return annotation_agreement_aggregate

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
