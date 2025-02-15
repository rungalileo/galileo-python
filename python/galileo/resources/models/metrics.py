from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Metrics")


@_attrs_define
class Metrics:
    """
    Attributes:
        bleu (Union[None, Unset, float]):
        context_relevance (Union[None, Unset, float]):
        factuality (Union[None, Unset, float]):
        groundedness (Union[None, Unset, float]):
        hallucination (Union[None, Unset, float]):
        instruction_adherence (Union[None, Unset, float]):
        latency (Union[None, Unset, float]):
        pii (Union[None, Unset, list[str]]):
        rouge (Union[None, Unset, float]):
        toxicity (Union[None, Unset, float]):
    """

    bleu: Union[None, Unset, float] = UNSET
    context_relevance: Union[None, Unset, float] = UNSET
    factuality: Union[None, Unset, float] = UNSET
    groundedness: Union[None, Unset, float] = UNSET
    hallucination: Union[None, Unset, float] = UNSET
    instruction_adherence: Union[None, Unset, float] = UNSET
    latency: Union[None, Unset, float] = UNSET
    pii: Union[None, Unset, list[str]] = UNSET
    rouge: Union[None, Unset, float] = UNSET
    toxicity: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bleu: Union[None, Unset, float]
        if isinstance(self.bleu, Unset):
            bleu = UNSET
        else:
            bleu = self.bleu

        context_relevance: Union[None, Unset, float]
        if isinstance(self.context_relevance, Unset):
            context_relevance = UNSET
        else:
            context_relevance = self.context_relevance

        factuality: Union[None, Unset, float]
        if isinstance(self.factuality, Unset):
            factuality = UNSET
        else:
            factuality = self.factuality

        groundedness: Union[None, Unset, float]
        if isinstance(self.groundedness, Unset):
            groundedness = UNSET
        else:
            groundedness = self.groundedness

        hallucination: Union[None, Unset, float]
        if isinstance(self.hallucination, Unset):
            hallucination = UNSET
        else:
            hallucination = self.hallucination

        instruction_adherence: Union[None, Unset, float]
        if isinstance(self.instruction_adherence, Unset):
            instruction_adherence = UNSET
        else:
            instruction_adherence = self.instruction_adherence

        latency: Union[None, Unset, float]
        if isinstance(self.latency, Unset):
            latency = UNSET
        else:
            latency = self.latency

        pii: Union[None, Unset, list[str]]
        if isinstance(self.pii, Unset):
            pii = UNSET
        elif isinstance(self.pii, list):
            pii = self.pii

        else:
            pii = self.pii

        rouge: Union[None, Unset, float]
        if isinstance(self.rouge, Unset):
            rouge = UNSET
        else:
            rouge = self.rouge

        toxicity: Union[None, Unset, float]
        if isinstance(self.toxicity, Unset):
            toxicity = UNSET
        else:
            toxicity = self.toxicity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bleu is not UNSET:
            field_dict["bleu"] = bleu
        if context_relevance is not UNSET:
            field_dict["context_relevance"] = context_relevance
        if factuality is not UNSET:
            field_dict["factuality"] = factuality
        if groundedness is not UNSET:
            field_dict["groundedness"] = groundedness
        if hallucination is not UNSET:
            field_dict["hallucination"] = hallucination
        if instruction_adherence is not UNSET:
            field_dict["instruction_adherence"] = instruction_adherence
        if latency is not UNSET:
            field_dict["latency"] = latency
        if pii is not UNSET:
            field_dict["pii"] = pii
        if rouge is not UNSET:
            field_dict["rouge"] = rouge
        if toxicity is not UNSET:
            field_dict["toxicity"] = toxicity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_bleu(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        bleu = _parse_bleu(d.pop("bleu", UNSET))

        def _parse_context_relevance(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        context_relevance = _parse_context_relevance(d.pop("context_relevance", UNSET))

        def _parse_factuality(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        factuality = _parse_factuality(d.pop("factuality", UNSET))

        def _parse_groundedness(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        groundedness = _parse_groundedness(d.pop("groundedness", UNSET))

        def _parse_hallucination(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        hallucination = _parse_hallucination(d.pop("hallucination", UNSET))

        def _parse_instruction_adherence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        instruction_adherence = _parse_instruction_adherence(d.pop("instruction_adherence", UNSET))

        def _parse_latency(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        latency = _parse_latency(d.pop("latency", UNSET))

        def _parse_pii(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                pii_type_0 = cast(list[str], data)

                return pii_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        pii = _parse_pii(d.pop("pii", UNSET))

        def _parse_rouge(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        rouge = _parse_rouge(d.pop("rouge", UNSET))

        def _parse_toxicity(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        toxicity = _parse_toxicity(d.pop("toxicity", UNSET))

        metrics = cls(
            bleu=bleu,
            context_relevance=context_relevance,
            factuality=factuality,
            groundedness=groundedness,
            hallucination=hallucination,
            instruction_adherence=instruction_adherence,
            latency=latency,
            pii=pii,
            rouge=rouge,
            toxicity=toxicity,
        )

        metrics.additional_properties = d
        return metrics

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
