from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chain_aggregation_strategy import ChainAggregationStrategy
from ..models.node_type import NodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_score import TestScore


T = TypeVar("T", bound="ValidResult")


@_attrs_define
class ValidResult:
    """
    Attributes
    ----------
        score_type (str):
        scoreable_node_types (list[NodeType]):
        test_scores (list['TestScore']):
        result_type (Union[Literal['valid'], Unset]):  Default: 'valid'.
        include_llm_credentials (Union[Unset, bool]):  Default: False.
        chain_aggregation (Union[ChainAggregationStrategy, None, Unset]):
    """

    score_type: str
    scoreable_node_types: list[NodeType]
    test_scores: list["TestScore"]
    result_type: Union[Literal["valid"], Unset] = "valid"
    include_llm_credentials: Union[Unset, bool] = False
    chain_aggregation: Union[ChainAggregationStrategy, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        score_type = self.score_type

        scoreable_node_types = []
        for scoreable_node_types_item_data in self.scoreable_node_types:
            scoreable_node_types_item = scoreable_node_types_item_data.value
            scoreable_node_types.append(scoreable_node_types_item)

        test_scores = []
        for test_scores_item_data in self.test_scores:
            test_scores_item = test_scores_item_data.to_dict()
            test_scores.append(test_scores_item)

        result_type = self.result_type

        include_llm_credentials = self.include_llm_credentials

        chain_aggregation: Union[None, Unset, str]
        if isinstance(self.chain_aggregation, Unset):
            chain_aggregation = UNSET
        elif isinstance(self.chain_aggregation, ChainAggregationStrategy):
            chain_aggregation = self.chain_aggregation.value
        else:
            chain_aggregation = self.chain_aggregation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"score_type": score_type, "scoreable_node_types": scoreable_node_types, "test_scores": test_scores}
        )
        if result_type is not UNSET:
            field_dict["result_type"] = result_type
        if include_llm_credentials is not UNSET:
            field_dict["include_llm_credentials"] = include_llm_credentials
        if chain_aggregation is not UNSET:
            field_dict["chain_aggregation"] = chain_aggregation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_score import TestScore

        d = dict(src_dict)
        score_type = d.pop("score_type")

        scoreable_node_types = []
        _scoreable_node_types = d.pop("scoreable_node_types")
        for scoreable_node_types_item_data in _scoreable_node_types:
            scoreable_node_types_item = NodeType(scoreable_node_types_item_data)

            scoreable_node_types.append(scoreable_node_types_item)

        test_scores = []
        _test_scores = d.pop("test_scores")
        for test_scores_item_data in _test_scores:
            test_scores_item = TestScore.from_dict(test_scores_item_data)

            test_scores.append(test_scores_item)

        result_type = cast(Union[Literal["valid"], Unset], d.pop("result_type", UNSET))
        if result_type != "valid" and not isinstance(result_type, Unset):
            raise ValueError(f"result_type must match const 'valid', got '{result_type}'")

        include_llm_credentials = d.pop("include_llm_credentials", UNSET)

        def _parse_chain_aggregation(data: object) -> Union[ChainAggregationStrategy, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ChainAggregationStrategy(data)

            except:  # noqa: E722
                pass
            return cast(Union[ChainAggregationStrategy, None, Unset], data)

        chain_aggregation = _parse_chain_aggregation(d.pop("chain_aggregation", UNSET))

        valid_result = cls(
            score_type=score_type,
            scoreable_node_types=scoreable_node_types,
            test_scores=test_scores,
            result_type=result_type,
            include_llm_credentials=include_llm_credentials,
            chain_aggregation=chain_aggregation,
        )

        valid_result.additional_properties = d
        return valid_result

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
