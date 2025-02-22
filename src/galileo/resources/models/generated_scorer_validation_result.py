from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GeneratedScorerValidationResult")


@_attrs_define
class GeneratedScorerValidationResult:
    """Result of a generated scorer validation job.

    Attributes:
        explanation (Union[None, str]):
        rating (Union[None, float]):
    """

    explanation: Union[None, str]
    rating: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        explanation: Union[None, str]
        explanation = self.explanation

        rating: Union[None, float]
        rating = self.rating

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"explanation": explanation, "rating": rating})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_explanation(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        explanation = _parse_explanation(d.pop("explanation"))

        def _parse_rating(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        rating = _parse_rating(d.pop("rating"))

        generated_scorer_validation_result = cls(explanation=explanation, rating=rating)

        generated_scorer_validation_result.additional_properties = d
        return generated_scorer_validation_result

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
