from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GeneratedScorerValidationResult")


@_attrs_define
class GeneratedScorerValidationResult:
    """Result of a generated scorer validation job.

    Attributes:
        rating (float | None | str):
        explanation (None | str):
    """

    rating: float | None | str
    explanation: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rating: float | None | str
        rating = self.rating

        explanation: None | str
        explanation = self.explanation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"rating": rating, "explanation": explanation})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_rating(data: object) -> float | None | str:
            if data is None:
                return data
            return cast(float | None | str, data)

        rating = _parse_rating(d.pop("rating"))

        def _parse_explanation(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        explanation = _parse_explanation(d.pop("explanation"))

        generated_scorer_validation_result = cls(rating=rating, explanation=explanation)

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
