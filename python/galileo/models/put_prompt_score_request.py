from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
        aggregates (Union['PutPromptScoreRequestAggregatesType0', None, Unset]):
        indices (Union[None, Unset, list[int]]):
        metric_name (Union[None, Unset, str]):
        registered_scorer_id (Union[None, Unset, str]):
        scores (Union[None, Unset, list[Any]]):
    """

    aggregates: Union["PutPromptScoreRequestAggregatesType0", None, Unset] = UNSET
    indices: Union[None, Unset, list[int]] = UNSET
    metric_name: Union[None, Unset, str] = UNSET
    registered_scorer_id: Union[None, Unset, str] = UNSET
    scores: Union[None, Unset, list[Any]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.put_prompt_score_request_aggregates_type_0 import PutPromptScoreRequestAggregatesType0

        aggregates: Union[None, Unset, dict[str, Any]]
        if isinstance(self.aggregates, Unset):
            aggregates = UNSET
        elif isinstance(self.aggregates, PutPromptScoreRequestAggregatesType0):
            aggregates = self.aggregates.to_dict()
        else:
            aggregates = self.aggregates

        indices: Union[None, Unset, list[int]]
        if isinstance(self.indices, Unset):
            indices = UNSET
        elif isinstance(self.indices, list):
            indices = self.indices

        else:
            indices = self.indices

        metric_name: Union[None, Unset, str]
        if isinstance(self.metric_name, Unset):
            metric_name = UNSET
        else:
            metric_name = self.metric_name

        registered_scorer_id: Union[None, Unset, str]
        if isinstance(self.registered_scorer_id, Unset):
            registered_scorer_id = UNSET
        else:
            registered_scorer_id = self.registered_scorer_id

        scores: Union[None, Unset, list[Any]]
        if isinstance(self.scores, Unset):
            scores = UNSET
        elif isinstance(self.scores, list):
            scores = self.scores

        else:
            scores = self.scores

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aggregates is not UNSET:
            field_dict["aggregates"] = aggregates
        if indices is not UNSET:
            field_dict["indices"] = indices
        if metric_name is not UNSET:
            field_dict["metric_name"] = metric_name
        if registered_scorer_id is not UNSET:
            field_dict["registered_scorer_id"] = registered_scorer_id
        if scores is not UNSET:
            field_dict["scores"] = scores

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.put_prompt_score_request_aggregates_type_0 import PutPromptScoreRequestAggregatesType0

        d = src_dict.copy()

        def _parse_aggregates(data: object) -> Union["PutPromptScoreRequestAggregatesType0", None, Unset]:
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
            return cast(Union["PutPromptScoreRequestAggregatesType0", None, Unset], data)

        aggregates = _parse_aggregates(d.pop("aggregates", UNSET))

        def _parse_indices(data: object) -> Union[None, Unset, list[int]]:
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
            return cast(Union[None, Unset, list[int]], data)

        indices = _parse_indices(d.pop("indices", UNSET))

        def _parse_metric_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metric_name = _parse_metric_name(d.pop("metric_name", UNSET))

        def _parse_registered_scorer_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        registered_scorer_id = _parse_registered_scorer_id(d.pop("registered_scorer_id", UNSET))

        def _parse_scores(data: object) -> Union[None, Unset, list[Any]]:
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
            return cast(Union[None, Unset, list[Any]], data)

        scores = _parse_scores(d.pop("scores", UNSET))

        put_prompt_score_request = cls(
            aggregates=aggregates,
            indices=indices,
            metric_name=metric_name,
            registered_scorer_id=registered_scorer_id,
            scores=scores,
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
