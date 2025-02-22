from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Seq2SeqMetricsResponse")


@_attrs_define
class Seq2SeqMetricsResponse:
    """Returns Seq2Seq specific metrics.

    Bleu and Rouge are the most common metrics for Seq2Seq models We also include average data error potential

        Attributes:
            average_bleu (Union[None, Unset, float]):
            average_data_error_potential (Union[None, Unset, float]):
            average_rouge (Union[None, Unset, float]):
    """

    average_bleu: Union[None, Unset, float] = UNSET
    average_data_error_potential: Union[None, Unset, float] = UNSET
    average_rouge: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        average_bleu: Union[None, Unset, float]
        if isinstance(self.average_bleu, Unset):
            average_bleu = UNSET
        else:
            average_bleu = self.average_bleu

        average_data_error_potential: Union[None, Unset, float]
        if isinstance(self.average_data_error_potential, Unset):
            average_data_error_potential = UNSET
        else:
            average_data_error_potential = self.average_data_error_potential

        average_rouge: Union[None, Unset, float]
        if isinstance(self.average_rouge, Unset):
            average_rouge = UNSET
        else:
            average_rouge = self.average_rouge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if average_bleu is not UNSET:
            field_dict["average_bleu"] = average_bleu
        if average_data_error_potential is not UNSET:
            field_dict["average_data_error_potential"] = average_data_error_potential
        if average_rouge is not UNSET:
            field_dict["average_rouge"] = average_rouge

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_average_bleu(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_bleu = _parse_average_bleu(d.pop("average_bleu", UNSET))

        def _parse_average_data_error_potential(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_data_error_potential = _parse_average_data_error_potential(d.pop("average_data_error_potential", UNSET))

        def _parse_average_rouge(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_rouge = _parse_average_rouge(d.pop("average_rouge", UNSET))

        seq_2_seq_metrics_response = cls(
            average_bleu=average_bleu,
            average_data_error_potential=average_data_error_potential,
            average_rouge=average_rouge,
        )

        seq_2_seq_metrics_response.additional_properties = d
        return seq_2_seq_metrics_response

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
