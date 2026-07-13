from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.scorer_version_health_score_entry import ScorerVersionHealthScoreEntry


T = TypeVar("T", bound="ScorerHealthScoresResponse")


@_attrs_define
class ScorerHealthScoresResponse:
    """
    Attributes
    ----------
        scores (list['ScorerVersionHealthScoreEntry']):
    """

    scores: list["ScorerVersionHealthScoreEntry"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scores = []
        for scores_item_data in self.scores:
            scores_item = scores_item_data.to_dict()
            scores.append(scores_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"scores": scores})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scorer_version_health_score_entry import ScorerVersionHealthScoreEntry

        d = dict(src_dict)
        scores = []
        _scores = d.pop("scores")
        for scores_item_data in _scores:
            scores_item = ScorerVersionHealthScoreEntry.from_dict(scores_item_data)

            scores.append(scores_item)

        scorer_health_scores_response = cls(scores=scores)

        scorer_health_scores_response.additional_properties = d
        return scorer_health_scores_response

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
