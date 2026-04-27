from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.put_prompt_score_request_aggregates_type_0 import PutPromptScoreRequestAggregatesType0


T = TypeVar("T", bound="PutPromptScoreRequest")


@_attrs_define
class PutPromptScoreRequest:
    """
    Attributes:
        metric_name (None | str | Unset):
        scores (list[Any] | None | Unset):
        indices (list[int] | None | Unset):
        aggregates (None | PutPromptScoreRequestAggregatesType0 | Unset):
        registered_scorer_id (None | str | Unset):
    """

    metric_name: None | str | Unset = UNSET
    scores: list[Any] | None | Unset = UNSET
    indices: list[int] | None | Unset = UNSET
    aggregates: None | PutPromptScoreRequestAggregatesType0 | Unset = UNSET
    registered_scorer_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.put_prompt_score_request_aggregates_type_0 import PutPromptScoreRequestAggregatesType0

        metric_name: None | str | Unset
        if isinstance(self.metric_name, Unset):
            metric_name = UNSET
        else:
            metric_name = self.metric_name

        scores: list[Any] | None | Unset
        if isinstance(self.scores, Unset):
            scores = UNSET
        elif isinstance(self.scores, list):
            scores = self.scores

        else:
            scores = self.scores

        indices: list[int] | None | Unset
        if isinstance(self.indices, Unset):
            indices = UNSET
        elif isinstance(self.indices, list):
            indices = self.indices

        else:
            indices = self.indices

        aggregates: dict[str, Any] | None | Unset
        if isinstance(self.aggregates, Unset):
            aggregates = UNSET
        elif isinstance(self.aggregates, PutPromptScoreRequestAggregatesType0):
            aggregates = self.aggregates.to_dict()
        else:
            aggregates = self.aggregates

        registered_scorer_id: None | str | Unset
        if isinstance(self.registered_scorer_id, Unset):
            registered_scorer_id = UNSET
        else:
            registered_scorer_id = self.registered_scorer_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metric_name is not UNSET:
            field_dict["metric_name"] = metric_name
        if scores is not UNSET:
            field_dict["scores"] = scores
        if indices is not UNSET:
            field_dict["indices"] = indices
        if aggregates is not UNSET:
            field_dict["aggregates"] = aggregates
        if registered_scorer_id is not UNSET:
            field_dict["registered_scorer_id"] = registered_scorer_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.put_prompt_score_request_aggregates_type_0 import PutPromptScoreRequestAggregatesType0

        d = dict(src_dict)

        def _parse_metric_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metric_name = _parse_metric_name(d.pop("metric_name", UNSET))

        def _parse_scores(data: object) -> list[Any] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scores_type_0 = cast(list[Any], data)

                return scores_type_0
            except:  # noqa: E722
                pass
            return cast(list[Any] | None | Unset, data)

        scores = _parse_scores(d.pop("scores", UNSET))

        def _parse_indices(data: object) -> list[int] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                indices_type_0 = cast(list[int], data)

                return indices_type_0
            except:  # noqa: E722
                pass
            return cast(list[int] | None | Unset, data)

        indices = _parse_indices(d.pop("indices", UNSET))

        def _parse_aggregates(data: object) -> None | PutPromptScoreRequestAggregatesType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregates_type_0 = PutPromptScoreRequestAggregatesType0.from_dict(data)

                return aggregates_type_0
            except:  # noqa: E722
                pass
            return cast(None | PutPromptScoreRequestAggregatesType0 | Unset, data)

        aggregates = _parse_aggregates(d.pop("aggregates", UNSET))

        def _parse_registered_scorer_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        registered_scorer_id = _parse_registered_scorer_id(d.pop("registered_scorer_id", UNSET))

        put_prompt_score_request = cls(
            metric_name=metric_name,
            scores=scores,
            indices=indices,
            aggregates=aggregates,
            registered_scorer_id=registered_scorer_id,
        )

        put_prompt_score_request.additional_properties = d
        return put_prompt_score_request

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
