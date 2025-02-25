from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.top_k_token import TopKToken


T = TypeVar("T", bound="Seq2SeqSegment")


@_attrs_define
class Seq2SeqSegment:
    """
    Attributes:
        end (int):
        start (int):
        data_error_potential (Union[None, Unset, float]):
        generated_uncertainty (Union[None, Unset, float]):
        segment_probability (Union[None, Unset, float]):
        top_k_tokens (Union[Unset, list['TopKToken']]):
    """

    end: int
    start: int
    data_error_potential: Union[None, Unset, float] = UNSET
    generated_uncertainty: Union[None, Unset, float] = UNSET
    segment_probability: Union[None, Unset, float] = UNSET
    top_k_tokens: Union[Unset, list["TopKToken"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        end = self.end

        start = self.start

        data_error_potential: Union[None, Unset, float]
        if isinstance(self.data_error_potential, Unset):
            data_error_potential = UNSET
        else:
            data_error_potential = self.data_error_potential

        generated_uncertainty: Union[None, Unset, float]
        if isinstance(self.generated_uncertainty, Unset):
            generated_uncertainty = UNSET
        else:
            generated_uncertainty = self.generated_uncertainty

        segment_probability: Union[None, Unset, float]
        if isinstance(self.segment_probability, Unset):
            segment_probability = UNSET
        else:
            segment_probability = self.segment_probability

        top_k_tokens: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.top_k_tokens, Unset):
            top_k_tokens = []
            for top_k_tokens_item_data in self.top_k_tokens:
                top_k_tokens_item = top_k_tokens_item_data.to_dict()
                top_k_tokens.append(top_k_tokens_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"end": end, "start": start})
        if data_error_potential is not UNSET:
            field_dict["data_error_potential"] = data_error_potential
        if generated_uncertainty is not UNSET:
            field_dict["generated_uncertainty"] = generated_uncertainty
        if segment_probability is not UNSET:
            field_dict["segment_probability"] = segment_probability
        if top_k_tokens is not UNSET:
            field_dict["top_k_tokens"] = top_k_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.top_k_token import TopKToken

        d = src_dict.copy()
        end = d.pop("end")

        start = d.pop("start")

        def _parse_data_error_potential(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        data_error_potential = _parse_data_error_potential(d.pop("data_error_potential", UNSET))

        def _parse_generated_uncertainty(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        generated_uncertainty = _parse_generated_uncertainty(d.pop("generated_uncertainty", UNSET))

        def _parse_segment_probability(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        segment_probability = _parse_segment_probability(d.pop("segment_probability", UNSET))

        top_k_tokens = []
        _top_k_tokens = d.pop("top_k_tokens", UNSET)
        for top_k_tokens_item_data in _top_k_tokens or []:
            top_k_tokens_item = TopKToken.from_dict(top_k_tokens_item_data)

            top_k_tokens.append(top_k_tokens_item)

        seq_2_seq_segment = cls(
            end=end,
            start=start,
            data_error_potential=data_error_potential,
            generated_uncertainty=generated_uncertainty,
            segment_probability=segment_probability,
            top_k_tokens=top_k_tokens,
        )

        seq_2_seq_segment.additional_properties = d
        return seq_2_seq_segment

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
