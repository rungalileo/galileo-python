from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.embedding_data_meta_type_0 import EmbeddingDataMetaType0


T = TypeVar("T", bound="EmbeddingData")


@_attrs_define
class EmbeddingData:
    """
    Attributes:
        id (int):
        x (float):
        y (float):
        bbox (Union[None, Unset, list[float]]):
        bleu (Union[None, Unset, float]):
        cluster_id (Union[None, Unset, int]):
        confidence (Union[None, Unset, float]):
        data_error_potential (Union[None, Unset, float]):
        drift_score (Union[None, Unset, float]):
        error_type (Union[None, Unset, str]):
        generated_output (Union[None, Unset, str]):
        generated_uncertainty (Union[None, Unset, float]):
        gold (Union[None, Unset, str]):
        image (Union[None, Unset, str]):
        input_ (Union[None, Unset, str]):
        is_gold (Union[None, Unset, bool]):
        is_pred (Union[None, Unset, bool]):
        meta (Union['EmbeddingDataMetaType0', None, Unset]):
        perplexity (Union[None, Unset, float]):
        pred (Union[None, Unset, str]):
        rouge (Union[None, Unset, float]):
        span_end (Union[None, Unset, int]):
        span_start (Union[None, Unset, int]):
        target (Union[None, Unset, str]):
        text_sample (Union[None, Unset, str]):
    """

    id: int
    x: float
    y: float
    bbox: Union[None, Unset, list[float]] = UNSET
    bleu: Union[None, Unset, float] = UNSET
    cluster_id: Union[None, Unset, int] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    data_error_potential: Union[None, Unset, float] = UNSET
    drift_score: Union[None, Unset, float] = UNSET
    error_type: Union[None, Unset, str] = UNSET
    generated_output: Union[None, Unset, str] = UNSET
    generated_uncertainty: Union[None, Unset, float] = UNSET
    gold: Union[None, Unset, str] = UNSET
    image: Union[None, Unset, str] = UNSET
    input_: Union[None, Unset, str] = UNSET
    is_gold: Union[None, Unset, bool] = UNSET
    is_pred: Union[None, Unset, bool] = UNSET
    meta: Union["EmbeddingDataMetaType0", None, Unset] = UNSET
    perplexity: Union[None, Unset, float] = UNSET
    pred: Union[None, Unset, str] = UNSET
    rouge: Union[None, Unset, float] = UNSET
    span_end: Union[None, Unset, int] = UNSET
    span_start: Union[None, Unset, int] = UNSET
    target: Union[None, Unset, str] = UNSET
    text_sample: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.embedding_data_meta_type_0 import EmbeddingDataMetaType0

        id = self.id

        x = self.x

        y = self.y

        bbox: Union[None, Unset, list[float]]
        if isinstance(self.bbox, Unset):
            bbox = UNSET
        elif isinstance(self.bbox, list):
            bbox = self.bbox

        else:
            bbox = self.bbox

        bleu: Union[None, Unset, float]
        if isinstance(self.bleu, Unset):
            bleu = UNSET
        else:
            bleu = self.bleu

        cluster_id: Union[None, Unset, int]
        if isinstance(self.cluster_id, Unset):
            cluster_id = UNSET
        else:
            cluster_id = self.cluster_id

        confidence: Union[None, Unset, float]
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        data_error_potential: Union[None, Unset, float]
        if isinstance(self.data_error_potential, Unset):
            data_error_potential = UNSET
        else:
            data_error_potential = self.data_error_potential

        drift_score: Union[None, Unset, float]
        if isinstance(self.drift_score, Unset):
            drift_score = UNSET
        else:
            drift_score = self.drift_score

        error_type: Union[None, Unset, str]
        if isinstance(self.error_type, Unset):
            error_type = UNSET
        else:
            error_type = self.error_type

        generated_output: Union[None, Unset, str]
        if isinstance(self.generated_output, Unset):
            generated_output = UNSET
        else:
            generated_output = self.generated_output

        generated_uncertainty: Union[None, Unset, float]
        if isinstance(self.generated_uncertainty, Unset):
            generated_uncertainty = UNSET
        else:
            generated_uncertainty = self.generated_uncertainty

        gold: Union[None, Unset, str]
        if isinstance(self.gold, Unset):
            gold = UNSET
        else:
            gold = self.gold

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        input_: Union[None, Unset, str]
        if isinstance(self.input_, Unset):
            input_ = UNSET
        else:
            input_ = self.input_

        is_gold: Union[None, Unset, bool]
        if isinstance(self.is_gold, Unset):
            is_gold = UNSET
        else:
            is_gold = self.is_gold

        is_pred: Union[None, Unset, bool]
        if isinstance(self.is_pred, Unset):
            is_pred = UNSET
        else:
            is_pred = self.is_pred

        meta: Union[None, Unset, dict[str, Any]]
        if isinstance(self.meta, Unset):
            meta = UNSET
        elif isinstance(self.meta, EmbeddingDataMetaType0):
            meta = self.meta.to_dict()
        else:
            meta = self.meta

        perplexity: Union[None, Unset, float]
        if isinstance(self.perplexity, Unset):
            perplexity = UNSET
        else:
            perplexity = self.perplexity

        pred: Union[None, Unset, str]
        if isinstance(self.pred, Unset):
            pred = UNSET
        else:
            pred = self.pred

        rouge: Union[None, Unset, float]
        if isinstance(self.rouge, Unset):
            rouge = UNSET
        else:
            rouge = self.rouge

        span_end: Union[None, Unset, int]
        if isinstance(self.span_end, Unset):
            span_end = UNSET
        else:
            span_end = self.span_end

        span_start: Union[None, Unset, int]
        if isinstance(self.span_start, Unset):
            span_start = UNSET
        else:
            span_start = self.span_start

        target: Union[None, Unset, str]
        if isinstance(self.target, Unset):
            target = UNSET
        else:
            target = self.target

        text_sample: Union[None, Unset, str]
        if isinstance(self.text_sample, Unset):
            text_sample = UNSET
        else:
            text_sample = self.text_sample

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "x": x, "y": y})
        if bbox is not UNSET:
            field_dict["bbox"] = bbox
        if bleu is not UNSET:
            field_dict["bleu"] = bleu
        if cluster_id is not UNSET:
            field_dict["cluster_id"] = cluster_id
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if data_error_potential is not UNSET:
            field_dict["data_error_potential"] = data_error_potential
        if drift_score is not UNSET:
            field_dict["drift_score"] = drift_score
        if error_type is not UNSET:
            field_dict["error_type"] = error_type
        if generated_output is not UNSET:
            field_dict["generated_output"] = generated_output
        if generated_uncertainty is not UNSET:
            field_dict["generated_uncertainty"] = generated_uncertainty
        if gold is not UNSET:
            field_dict["gold"] = gold
        if image is not UNSET:
            field_dict["image"] = image
        if input_ is not UNSET:
            field_dict["input"] = input_
        if is_gold is not UNSET:
            field_dict["is_gold"] = is_gold
        if is_pred is not UNSET:
            field_dict["is_pred"] = is_pred
        if meta is not UNSET:
            field_dict["meta"] = meta
        if perplexity is not UNSET:
            field_dict["perplexity"] = perplexity
        if pred is not UNSET:
            field_dict["pred"] = pred
        if rouge is not UNSET:
            field_dict["rouge"] = rouge
        if span_end is not UNSET:
            field_dict["span_end"] = span_end
        if span_start is not UNSET:
            field_dict["span_start"] = span_start
        if target is not UNSET:
            field_dict["target"] = target
        if text_sample is not UNSET:
            field_dict["text_sample"] = text_sample

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.embedding_data_meta_type_0 import EmbeddingDataMetaType0

        d = src_dict.copy()
        id = d.pop("id")

        x = d.pop("x")

        y = d.pop("y")

        def _parse_bbox(data: object) -> Union[None, Unset, list[float]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                bbox_type_0 = cast(list[float], data)

                return bbox_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[float]], data)

        bbox = _parse_bbox(d.pop("bbox", UNSET))

        def _parse_bleu(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        bleu = _parse_bleu(d.pop("bleu", UNSET))

        def _parse_cluster_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        cluster_id = _parse_cluster_id(d.pop("cluster_id", UNSET))

        def _parse_confidence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        def _parse_data_error_potential(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        data_error_potential = _parse_data_error_potential(d.pop("data_error_potential", UNSET))

        def _parse_drift_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        drift_score = _parse_drift_score(d.pop("drift_score", UNSET))

        def _parse_error_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_type = _parse_error_type(d.pop("error_type", UNSET))

        def _parse_generated_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        generated_output = _parse_generated_output(d.pop("generated_output", UNSET))

        def _parse_generated_uncertainty(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        generated_uncertainty = _parse_generated_uncertainty(d.pop("generated_uncertainty", UNSET))

        def _parse_gold(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        gold = _parse_gold(d.pop("gold", UNSET))

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        def _parse_input_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_ = _parse_input_(d.pop("input", UNSET))

        def _parse_is_gold(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_gold = _parse_is_gold(d.pop("is_gold", UNSET))

        def _parse_is_pred(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_pred = _parse_is_pred(d.pop("is_pred", UNSET))

        def _parse_meta(data: object) -> Union["EmbeddingDataMetaType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                meta_type_0 = EmbeddingDataMetaType0.from_dict(data)

                return meta_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EmbeddingDataMetaType0", None, Unset], data)

        meta = _parse_meta(d.pop("meta", UNSET))

        def _parse_perplexity(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        perplexity = _parse_perplexity(d.pop("perplexity", UNSET))

        def _parse_pred(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pred = _parse_pred(d.pop("pred", UNSET))

        def _parse_rouge(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        rouge = _parse_rouge(d.pop("rouge", UNSET))

        def _parse_span_end(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        span_end = _parse_span_end(d.pop("span_end", UNSET))

        def _parse_span_start(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        span_start = _parse_span_start(d.pop("span_start", UNSET))

        def _parse_target(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        target = _parse_target(d.pop("target", UNSET))

        def _parse_text_sample(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        text_sample = _parse_text_sample(d.pop("text_sample", UNSET))

        embedding_data = cls(
            id=id,
            x=x,
            y=y,
            bbox=bbox,
            bleu=bleu,
            cluster_id=cluster_id,
            confidence=confidence,
            data_error_potential=data_error_potential,
            drift_score=drift_score,
            error_type=error_type,
            generated_output=generated_output,
            generated_uncertainty=generated_uncertainty,
            gold=gold,
            image=image,
            input_=input_,
            is_gold=is_gold,
            is_pred=is_pred,
            meta=meta,
            perplexity=perplexity,
            pred=pred,
            rouge=rouge,
            span_end=span_end,
            span_start=span_start,
            target=target,
            text_sample=text_sample,
        )

        embedding_data.additional_properties = d
        return embedding_data

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
