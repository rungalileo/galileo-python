from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CommunityResponse")


@_attrs_define
class CommunityResponse:
    """See `rungalileo.schemas.content.insights.Community` for details on Communities.

    Before returning the results to the UI, we scale the continuous community score to
    an int for better interpretability for the user.

    0-0.03 = 1
    0.03-0.07 = 2
    0.07-0.15 = 3
    0.15-0.2=4
    0.2=5

        Attributes:
            labels (list[str]):
            num_samples (int):
            score (int):
    """

    labels: list[str]
    num_samples: int
    score: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        labels = self.labels

        num_samples = self.num_samples

        score = self.score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"labels": labels, "num_samples": num_samples, "score": score})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        labels = cast(list[str], d.pop("labels"))

        num_samples = d.pop("num_samples")

        score = d.pop("score")

        community_response = cls(labels=labels, num_samples=num_samples, score=score)

        community_response.additional_properties = d
        return community_response

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
