from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metric_critique_scorer import MetricCritiqueScorer


T = TypeVar("T", bound="MetricCritiqueScorers")


@_attrs_define
class MetricCritiqueScorers:
    """
    Attributes:
        scorers (list[MetricCritiqueScorer]):
    """

    scorers: list[MetricCritiqueScorer]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scorers = []
        for scorers_item_data in self.scorers:
            scorers_item = scorers_item_data.to_dict()
            scorers.append(scorers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"scorers": scorers})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_critique_scorer import MetricCritiqueScorer

        d = dict(src_dict)
        scorers = []
        _scorers = d.pop("scorers")
        for scorers_item_data in _scorers:
            scorers_item = MetricCritiqueScorer.from_dict(scorers_item_data)

            scorers.append(scorers_item)

        metric_critique_scorers = cls(scorers=scorers)

        metric_critique_scorers.additional_properties = d
        return metric_critique_scorers

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
