from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.noise_type import NoiseType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.b_box import BBox
    from ..models.data_row_meta_type_0 import DataRowMetaType0
    from ..models.data_row_system_prompts_type_0 import DataRowSystemPromptsType0
    from ..models.polygon_data import PolygonData
    from ..models.seq_2_seq_segment import Seq2SeqSegment
    from ..models.span import Span


T = TypeVar("T", bound="DataRow")


@_attrs_define
class DataRow:
    """
    Attributes:
        id (int):
        background (Union[None, Unset, int]):
        bleu (Union[None, Unset, float]):
        boundary_iou (Union[None, Unset, float]):
        boxes (Union[None, Unset, list['BBox']]):
        classification (Union[None, Unset, int]):
        classification_and_localization (Union[None, Unset, int]):
        confidence (Union[None, Unset, float]):
        data_error_potential (Union[None, Unset, float]):
        dep_mask (Union[None, Unset, str]):
        drift_score (Union[None, Unset, float]):
        duplicate (Union[None, Unset, int]):
        edit_relabeled (Union[Unset, bool]):  Default: False.
        edited (Union[Unset, bool]):  Default: False.
        generated_output (Union[None, Unset, str]):
        generated_segments (Union[None, Unset, list['Seq2SeqSegment']]):
        generated_uncertainty (Union[None, Unset, float]):
        ghost_span (Union[None, Unset, int]):
        gold (Union[None, Unset, str]):
        height (Union[None, Unset, int]):
        image (Union[None, Unset, str]):  Default: ''.
        input_ (Union[None, Unset, str]):
        input_cutoff (Union[None, Unset, int]):
        is_drifted (Union[None, Unset, bool]):
        is_on_the_boundary (Union[None, Unset, bool]):
        localization (Union[None, Unset, int]):
        max_dep (Union[None, Unset, float]):
        max_dep_label (Union[None, Unset, str]):
        mean_iou (Union[None, Unset, float]):
        meta (Union['DataRowMetaType0', None, Unset]):
        missed (Union[None, Unset, int]):
        missed_label (Union[None, Unset, int]):
        mltc_golds (Union[None, Unset, list[str]]):
        mltc_golds_deps (Union[None, Unset, list[float]]):
        mltc_preds (Union[None, Unset, list[str]]):
        mltc_preds_deps (Union[None, Unset, list[float]]):
        noise_type (Union[NoiseType, None, Unset]):
        perplexity (Union[None, Unset, float]):
        polygons (Union[None, Unset, list['PolygonData']]):
        pred (Union[None, Unset, str]):
        rouge (Union[None, Unset, float]):
        span_shift (Union[None, Unset, int]):
        spans (Union[None, Unset, list['Span']]):
        system_prompts (Union['DataRowSystemPromptsType0', None, Unset]):
        target (Union[None, Unset, str]):
        target_cutoff (Union[None, Unset, int]):
        target_segments (Union[None, Unset, list['Seq2SeqSegment']]):
        text (Union[None, Unset, str]):  Default: ''.
        total_errors (Union[None, Unset, int]):
        width (Union[None, Unset, int]):
        wrong_tag (Union[None, Unset, int]):
        x (Union[None, Unset, float]):
        y (Union[None, Unset, float]):
    """

    id: int
    background: Union[None, Unset, int] = UNSET
    bleu: Union[None, Unset, float] = UNSET
    boundary_iou: Union[None, Unset, float] = UNSET
    boxes: Union[None, Unset, list["BBox"]] = UNSET
    classification: Union[None, Unset, int] = UNSET
    classification_and_localization: Union[None, Unset, int] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    data_error_potential: Union[None, Unset, float] = UNSET
    dep_mask: Union[None, Unset, str] = UNSET
    drift_score: Union[None, Unset, float] = UNSET
    duplicate: Union[None, Unset, int] = UNSET
    edit_relabeled: Union[Unset, bool] = False
    edited: Union[Unset, bool] = False
    generated_output: Union[None, Unset, str] = UNSET
    generated_segments: Union[None, Unset, list["Seq2SeqSegment"]] = UNSET
    generated_uncertainty: Union[None, Unset, float] = UNSET
    ghost_span: Union[None, Unset, int] = UNSET
    gold: Union[None, Unset, str] = UNSET
    height: Union[None, Unset, int] = UNSET
    image: Union[None, Unset, str] = ""
    input_: Union[None, Unset, str] = UNSET
    input_cutoff: Union[None, Unset, int] = UNSET
    is_drifted: Union[None, Unset, bool] = UNSET
    is_on_the_boundary: Union[None, Unset, bool] = UNSET
    localization: Union[None, Unset, int] = UNSET
    max_dep: Union[None, Unset, float] = UNSET
    max_dep_label: Union[None, Unset, str] = UNSET
    mean_iou: Union[None, Unset, float] = UNSET
    meta: Union["DataRowMetaType0", None, Unset] = UNSET
    missed: Union[None, Unset, int] = UNSET
    missed_label: Union[None, Unset, int] = UNSET
    mltc_golds: Union[None, Unset, list[str]] = UNSET
    mltc_golds_deps: Union[None, Unset, list[float]] = UNSET
    mltc_preds: Union[None, Unset, list[str]] = UNSET
    mltc_preds_deps: Union[None, Unset, list[float]] = UNSET
    noise_type: Union[NoiseType, None, Unset] = UNSET
    perplexity: Union[None, Unset, float] = UNSET
    polygons: Union[None, Unset, list["PolygonData"]] = UNSET
    pred: Union[None, Unset, str] = UNSET
    rouge: Union[None, Unset, float] = UNSET
    span_shift: Union[None, Unset, int] = UNSET
    spans: Union[None, Unset, list["Span"]] = UNSET
    system_prompts: Union["DataRowSystemPromptsType0", None, Unset] = UNSET
    target: Union[None, Unset, str] = UNSET
    target_cutoff: Union[None, Unset, int] = UNSET
    target_segments: Union[None, Unset, list["Seq2SeqSegment"]] = UNSET
    text: Union[None, Unset, str] = ""
    total_errors: Union[None, Unset, int] = UNSET
    width: Union[None, Unset, int] = UNSET
    wrong_tag: Union[None, Unset, int] = UNSET
    x: Union[None, Unset, float] = UNSET
    y: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.data_row_meta_type_0 import DataRowMetaType0
        from ..models.data_row_system_prompts_type_0 import DataRowSystemPromptsType0

        id = self.id

        background: Union[None, Unset, int]
        if isinstance(self.background, Unset):
            background = UNSET
        else:
            background = self.background

        bleu: Union[None, Unset, float]
        if isinstance(self.bleu, Unset):
            bleu = UNSET
        else:
            bleu = self.bleu

        boundary_iou: Union[None, Unset, float]
        if isinstance(self.boundary_iou, Unset):
            boundary_iou = UNSET
        else:
            boundary_iou = self.boundary_iou

        boxes: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.boxes, Unset):
            boxes = UNSET
        elif isinstance(self.boxes, list):
            boxes = []
            for boxes_type_0_item_data in self.boxes:
                boxes_type_0_item = boxes_type_0_item_data.to_dict()
                boxes.append(boxes_type_0_item)

        else:
            boxes = self.boxes

        classification: Union[None, Unset, int]
        if isinstance(self.classification, Unset):
            classification = UNSET
        else:
            classification = self.classification

        classification_and_localization: Union[None, Unset, int]
        if isinstance(self.classification_and_localization, Unset):
            classification_and_localization = UNSET
        else:
            classification_and_localization = self.classification_and_localization

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

        dep_mask: Union[None, Unset, str]
        if isinstance(self.dep_mask, Unset):
            dep_mask = UNSET
        else:
            dep_mask = self.dep_mask

        drift_score: Union[None, Unset, float]
        if isinstance(self.drift_score, Unset):
            drift_score = UNSET
        else:
            drift_score = self.drift_score

        duplicate: Union[None, Unset, int]
        if isinstance(self.duplicate, Unset):
            duplicate = UNSET
        else:
            duplicate = self.duplicate

        edit_relabeled = self.edit_relabeled

        edited = self.edited

        generated_output: Union[None, Unset, str]
        if isinstance(self.generated_output, Unset):
            generated_output = UNSET
        else:
            generated_output = self.generated_output

        generated_segments: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.generated_segments, Unset):
            generated_segments = UNSET
        elif isinstance(self.generated_segments, list):
            generated_segments = []
            for generated_segments_type_0_item_data in self.generated_segments:
                generated_segments_type_0_item = generated_segments_type_0_item_data.to_dict()
                generated_segments.append(generated_segments_type_0_item)

        else:
            generated_segments = self.generated_segments

        generated_uncertainty: Union[None, Unset, float]
        if isinstance(self.generated_uncertainty, Unset):
            generated_uncertainty = UNSET
        else:
            generated_uncertainty = self.generated_uncertainty

        ghost_span: Union[None, Unset, int]
        if isinstance(self.ghost_span, Unset):
            ghost_span = UNSET
        else:
            ghost_span = self.ghost_span

        gold: Union[None, Unset, str]
        if isinstance(self.gold, Unset):
            gold = UNSET
        else:
            gold = self.gold

        height: Union[None, Unset, int]
        if isinstance(self.height, Unset):
            height = UNSET
        else:
            height = self.height

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

        input_cutoff: Union[None, Unset, int]
        if isinstance(self.input_cutoff, Unset):
            input_cutoff = UNSET
        else:
            input_cutoff = self.input_cutoff

        is_drifted: Union[None, Unset, bool]
        if isinstance(self.is_drifted, Unset):
            is_drifted = UNSET
        else:
            is_drifted = self.is_drifted

        is_on_the_boundary: Union[None, Unset, bool]
        if isinstance(self.is_on_the_boundary, Unset):
            is_on_the_boundary = UNSET
        else:
            is_on_the_boundary = self.is_on_the_boundary

        localization: Union[None, Unset, int]
        if isinstance(self.localization, Unset):
            localization = UNSET
        else:
            localization = self.localization

        max_dep: Union[None, Unset, float]
        if isinstance(self.max_dep, Unset):
            max_dep = UNSET
        else:
            max_dep = self.max_dep

        max_dep_label: Union[None, Unset, str]
        if isinstance(self.max_dep_label, Unset):
            max_dep_label = UNSET
        else:
            max_dep_label = self.max_dep_label

        mean_iou: Union[None, Unset, float]
        if isinstance(self.mean_iou, Unset):
            mean_iou = UNSET
        else:
            mean_iou = self.mean_iou

        meta: Union[None, Unset, dict[str, Any]]
        if isinstance(self.meta, Unset):
            meta = UNSET
        elif isinstance(self.meta, DataRowMetaType0):
            meta = self.meta.to_dict()
        else:
            meta = self.meta

        missed: Union[None, Unset, int]
        if isinstance(self.missed, Unset):
            missed = UNSET
        else:
            missed = self.missed

        missed_label: Union[None, Unset, int]
        if isinstance(self.missed_label, Unset):
            missed_label = UNSET
        else:
            missed_label = self.missed_label

        mltc_golds: Union[None, Unset, list[str]]
        if isinstance(self.mltc_golds, Unset):
            mltc_golds = UNSET
        elif isinstance(self.mltc_golds, list):
            mltc_golds = self.mltc_golds

        else:
            mltc_golds = self.mltc_golds

        mltc_golds_deps: Union[None, Unset, list[float]]
        if isinstance(self.mltc_golds_deps, Unset):
            mltc_golds_deps = UNSET
        elif isinstance(self.mltc_golds_deps, list):
            mltc_golds_deps = self.mltc_golds_deps

        else:
            mltc_golds_deps = self.mltc_golds_deps

        mltc_preds: Union[None, Unset, list[str]]
        if isinstance(self.mltc_preds, Unset):
            mltc_preds = UNSET
        elif isinstance(self.mltc_preds, list):
            mltc_preds = self.mltc_preds

        else:
            mltc_preds = self.mltc_preds

        mltc_preds_deps: Union[None, Unset, list[float]]
        if isinstance(self.mltc_preds_deps, Unset):
            mltc_preds_deps = UNSET
        elif isinstance(self.mltc_preds_deps, list):
            mltc_preds_deps = self.mltc_preds_deps

        else:
            mltc_preds_deps = self.mltc_preds_deps

        noise_type: Union[None, Unset, str]
        if isinstance(self.noise_type, Unset):
            noise_type = UNSET
        elif isinstance(self.noise_type, NoiseType):
            noise_type = self.noise_type.value
        else:
            noise_type = self.noise_type

        perplexity: Union[None, Unset, float]
        if isinstance(self.perplexity, Unset):
            perplexity = UNSET
        else:
            perplexity = self.perplexity

        polygons: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.polygons, Unset):
            polygons = UNSET
        elif isinstance(self.polygons, list):
            polygons = []
            for polygons_type_0_item_data in self.polygons:
                polygons_type_0_item = polygons_type_0_item_data.to_dict()
                polygons.append(polygons_type_0_item)

        else:
            polygons = self.polygons

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

        span_shift: Union[None, Unset, int]
        if isinstance(self.span_shift, Unset):
            span_shift = UNSET
        else:
            span_shift = self.span_shift

        spans: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.spans, Unset):
            spans = UNSET
        elif isinstance(self.spans, list):
            spans = []
            for spans_type_0_item_data in self.spans:
                spans_type_0_item = spans_type_0_item_data.to_dict()
                spans.append(spans_type_0_item)

        else:
            spans = self.spans

        system_prompts: Union[None, Unset, dict[str, Any]]
        if isinstance(self.system_prompts, Unset):
            system_prompts = UNSET
        elif isinstance(self.system_prompts, DataRowSystemPromptsType0):
            system_prompts = self.system_prompts.to_dict()
        else:
            system_prompts = self.system_prompts

        target: Union[None, Unset, str]
        if isinstance(self.target, Unset):
            target = UNSET
        else:
            target = self.target

        target_cutoff: Union[None, Unset, int]
        if isinstance(self.target_cutoff, Unset):
            target_cutoff = UNSET
        else:
            target_cutoff = self.target_cutoff

        target_segments: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.target_segments, Unset):
            target_segments = UNSET
        elif isinstance(self.target_segments, list):
            target_segments = []
            for target_segments_type_0_item_data in self.target_segments:
                target_segments_type_0_item = target_segments_type_0_item_data.to_dict()
                target_segments.append(target_segments_type_0_item)

        else:
            target_segments = self.target_segments

        text: Union[None, Unset, str]
        if isinstance(self.text, Unset):
            text = UNSET
        else:
            text = self.text

        total_errors: Union[None, Unset, int]
        if isinstance(self.total_errors, Unset):
            total_errors = UNSET
        else:
            total_errors = self.total_errors

        width: Union[None, Unset, int]
        if isinstance(self.width, Unset):
            width = UNSET
        else:
            width = self.width

        wrong_tag: Union[None, Unset, int]
        if isinstance(self.wrong_tag, Unset):
            wrong_tag = UNSET
        else:
            wrong_tag = self.wrong_tag

        x: Union[None, Unset, float]
        if isinstance(self.x, Unset):
            x = UNSET
        else:
            x = self.x

        y: Union[None, Unset, float]
        if isinstance(self.y, Unset):
            y = UNSET
        else:
            y = self.y

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id})
        if background is not UNSET:
            field_dict["background"] = background
        if bleu is not UNSET:
            field_dict["bleu"] = bleu
        if boundary_iou is not UNSET:
            field_dict["boundary_iou"] = boundary_iou
        if boxes is not UNSET:
            field_dict["boxes"] = boxes
        if classification is not UNSET:
            field_dict["classification"] = classification
        if classification_and_localization is not UNSET:
            field_dict["classification_and_localization"] = classification_and_localization
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if data_error_potential is not UNSET:
            field_dict["data_error_potential"] = data_error_potential
        if dep_mask is not UNSET:
            field_dict["dep_mask"] = dep_mask
        if drift_score is not UNSET:
            field_dict["drift_score"] = drift_score
        if duplicate is not UNSET:
            field_dict["duplicate"] = duplicate
        if edit_relabeled is not UNSET:
            field_dict["edit_relabeled"] = edit_relabeled
        if edited is not UNSET:
            field_dict["edited"] = edited
        if generated_output is not UNSET:
            field_dict["generated_output"] = generated_output
        if generated_segments is not UNSET:
            field_dict["generated_segments"] = generated_segments
        if generated_uncertainty is not UNSET:
            field_dict["generated_uncertainty"] = generated_uncertainty
        if ghost_span is not UNSET:
            field_dict["ghost_span"] = ghost_span
        if gold is not UNSET:
            field_dict["gold"] = gold
        if height is not UNSET:
            field_dict["height"] = height
        if image is not UNSET:
            field_dict["image"] = image
        if input_ is not UNSET:
            field_dict["input"] = input_
        if input_cutoff is not UNSET:
            field_dict["input_cutoff"] = input_cutoff
        if is_drifted is not UNSET:
            field_dict["is_drifted"] = is_drifted
        if is_on_the_boundary is not UNSET:
            field_dict["is_on_the_boundary"] = is_on_the_boundary
        if localization is not UNSET:
            field_dict["localization"] = localization
        if max_dep is not UNSET:
            field_dict["max_dep"] = max_dep
        if max_dep_label is not UNSET:
            field_dict["max_dep_label"] = max_dep_label
        if mean_iou is not UNSET:
            field_dict["mean_iou"] = mean_iou
        if meta is not UNSET:
            field_dict["meta"] = meta
        if missed is not UNSET:
            field_dict["missed"] = missed
        if missed_label is not UNSET:
            field_dict["missed_label"] = missed_label
        if mltc_golds is not UNSET:
            field_dict["mltc_golds"] = mltc_golds
        if mltc_golds_deps is not UNSET:
            field_dict["mltc_golds_deps"] = mltc_golds_deps
        if mltc_preds is not UNSET:
            field_dict["mltc_preds"] = mltc_preds
        if mltc_preds_deps is not UNSET:
            field_dict["mltc_preds_deps"] = mltc_preds_deps
        if noise_type is not UNSET:
            field_dict["noise_type"] = noise_type
        if perplexity is not UNSET:
            field_dict["perplexity"] = perplexity
        if polygons is not UNSET:
            field_dict["polygons"] = polygons
        if pred is not UNSET:
            field_dict["pred"] = pred
        if rouge is not UNSET:
            field_dict["rouge"] = rouge
        if span_shift is not UNSET:
            field_dict["span_shift"] = span_shift
        if spans is not UNSET:
            field_dict["spans"] = spans
        if system_prompts is not UNSET:
            field_dict["system_prompts"] = system_prompts
        if target is not UNSET:
            field_dict["target"] = target
        if target_cutoff is not UNSET:
            field_dict["target_cutoff"] = target_cutoff
        if target_segments is not UNSET:
            field_dict["target_segments"] = target_segments
        if text is not UNSET:
            field_dict["text"] = text
        if total_errors is not UNSET:
            field_dict["total_errors"] = total_errors
        if width is not UNSET:
            field_dict["width"] = width
        if wrong_tag is not UNSET:
            field_dict["wrong_tag"] = wrong_tag
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.b_box import BBox
        from ..models.data_row_meta_type_0 import DataRowMetaType0
        from ..models.data_row_system_prompts_type_0 import DataRowSystemPromptsType0
        from ..models.polygon_data import PolygonData
        from ..models.seq_2_seq_segment import Seq2SeqSegment
        from ..models.span import Span

        d = src_dict.copy()
        id = d.pop("id")

        def _parse_background(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        background = _parse_background(d.pop("background", UNSET))

        def _parse_bleu(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        bleu = _parse_bleu(d.pop("bleu", UNSET))

        def _parse_boundary_iou(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        boundary_iou = _parse_boundary_iou(d.pop("boundary_iou", UNSET))

        def _parse_boxes(data: object) -> Union[None, Unset, list["BBox"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                boxes_type_0 = []
                _boxes_type_0 = data
                for boxes_type_0_item_data in _boxes_type_0:
                    boxes_type_0_item = BBox.from_dict(boxes_type_0_item_data)

                    boxes_type_0.append(boxes_type_0_item)

                return boxes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["BBox"]], data)

        boxes = _parse_boxes(d.pop("boxes", UNSET))

        def _parse_classification(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        classification = _parse_classification(d.pop("classification", UNSET))

        def _parse_classification_and_localization(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        classification_and_localization = _parse_classification_and_localization(
            d.pop("classification_and_localization", UNSET)
        )

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

        def _parse_dep_mask(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dep_mask = _parse_dep_mask(d.pop("dep_mask", UNSET))

        def _parse_drift_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        drift_score = _parse_drift_score(d.pop("drift_score", UNSET))

        def _parse_duplicate(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        duplicate = _parse_duplicate(d.pop("duplicate", UNSET))

        edit_relabeled = d.pop("edit_relabeled", UNSET)

        edited = d.pop("edited", UNSET)

        def _parse_generated_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        generated_output = _parse_generated_output(d.pop("generated_output", UNSET))

        def _parse_generated_segments(data: object) -> Union[None, Unset, list["Seq2SeqSegment"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                generated_segments_type_0 = []
                _generated_segments_type_0 = data
                for generated_segments_type_0_item_data in _generated_segments_type_0:
                    generated_segments_type_0_item = Seq2SeqSegment.from_dict(generated_segments_type_0_item_data)

                    generated_segments_type_0.append(generated_segments_type_0_item)

                return generated_segments_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Seq2SeqSegment"]], data)

        generated_segments = _parse_generated_segments(d.pop("generated_segments", UNSET))

        def _parse_generated_uncertainty(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        generated_uncertainty = _parse_generated_uncertainty(d.pop("generated_uncertainty", UNSET))

        def _parse_ghost_span(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        ghost_span = _parse_ghost_span(d.pop("ghost_span", UNSET))

        def _parse_gold(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        gold = _parse_gold(d.pop("gold", UNSET))

        def _parse_height(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        height = _parse_height(d.pop("height", UNSET))

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

        def _parse_input_cutoff(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        input_cutoff = _parse_input_cutoff(d.pop("input_cutoff", UNSET))

        def _parse_is_drifted(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_drifted = _parse_is_drifted(d.pop("is_drifted", UNSET))

        def _parse_is_on_the_boundary(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_on_the_boundary = _parse_is_on_the_boundary(d.pop("is_on_the_boundary", UNSET))

        def _parse_localization(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        localization = _parse_localization(d.pop("localization", UNSET))

        def _parse_max_dep(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        max_dep = _parse_max_dep(d.pop("max_dep", UNSET))

        def _parse_max_dep_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        max_dep_label = _parse_max_dep_label(d.pop("max_dep_label", UNSET))

        def _parse_mean_iou(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        mean_iou = _parse_mean_iou(d.pop("mean_iou", UNSET))

        def _parse_meta(data: object) -> Union["DataRowMetaType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                meta_type_0 = DataRowMetaType0.from_dict(data)

                return meta_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DataRowMetaType0", None, Unset], data)

        meta = _parse_meta(d.pop("meta", UNSET))

        def _parse_missed(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        missed = _parse_missed(d.pop("missed", UNSET))

        def _parse_missed_label(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        missed_label = _parse_missed_label(d.pop("missed_label", UNSET))

        def _parse_mltc_golds(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                mltc_golds_type_0 = cast(list[str], data)

                return mltc_golds_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        mltc_golds = _parse_mltc_golds(d.pop("mltc_golds", UNSET))

        def _parse_mltc_golds_deps(data: object) -> Union[None, Unset, list[float]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                mltc_golds_deps_type_0 = cast(list[float], data)

                return mltc_golds_deps_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[float]], data)

        mltc_golds_deps = _parse_mltc_golds_deps(d.pop("mltc_golds_deps", UNSET))

        def _parse_mltc_preds(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                mltc_preds_type_0 = cast(list[str], data)

                return mltc_preds_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        mltc_preds = _parse_mltc_preds(d.pop("mltc_preds", UNSET))

        def _parse_mltc_preds_deps(data: object) -> Union[None, Unset, list[float]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                mltc_preds_deps_type_0 = cast(list[float], data)

                return mltc_preds_deps_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[float]], data)

        mltc_preds_deps = _parse_mltc_preds_deps(d.pop("mltc_preds_deps", UNSET))

        def _parse_noise_type(data: object) -> Union[NoiseType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                noise_type_type_0 = NoiseType(data)

                return noise_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[NoiseType, None, Unset], data)

        noise_type = _parse_noise_type(d.pop("noise_type", UNSET))

        def _parse_perplexity(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        perplexity = _parse_perplexity(d.pop("perplexity", UNSET))

        def _parse_polygons(data: object) -> Union[None, Unset, list["PolygonData"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                polygons_type_0 = []
                _polygons_type_0 = data
                for polygons_type_0_item_data in _polygons_type_0:
                    polygons_type_0_item = PolygonData.from_dict(polygons_type_0_item_data)

                    polygons_type_0.append(polygons_type_0_item)

                return polygons_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["PolygonData"]], data)

        polygons = _parse_polygons(d.pop("polygons", UNSET))

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

        def _parse_span_shift(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        span_shift = _parse_span_shift(d.pop("span_shift", UNSET))

        def _parse_spans(data: object) -> Union[None, Unset, list["Span"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                spans_type_0 = []
                _spans_type_0 = data
                for spans_type_0_item_data in _spans_type_0:
                    spans_type_0_item = Span.from_dict(spans_type_0_item_data)

                    spans_type_0.append(spans_type_0_item)

                return spans_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Span"]], data)

        spans = _parse_spans(d.pop("spans", UNSET))

        def _parse_system_prompts(data: object) -> Union["DataRowSystemPromptsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                system_prompts_type_0 = DataRowSystemPromptsType0.from_dict(data)

                return system_prompts_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DataRowSystemPromptsType0", None, Unset], data)

        system_prompts = _parse_system_prompts(d.pop("system_prompts", UNSET))

        def _parse_target(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        target = _parse_target(d.pop("target", UNSET))

        def _parse_target_cutoff(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        target_cutoff = _parse_target_cutoff(d.pop("target_cutoff", UNSET))

        def _parse_target_segments(data: object) -> Union[None, Unset, list["Seq2SeqSegment"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                target_segments_type_0 = []
                _target_segments_type_0 = data
                for target_segments_type_0_item_data in _target_segments_type_0:
                    target_segments_type_0_item = Seq2SeqSegment.from_dict(target_segments_type_0_item_data)

                    target_segments_type_0.append(target_segments_type_0_item)

                return target_segments_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Seq2SeqSegment"]], data)

        target_segments = _parse_target_segments(d.pop("target_segments", UNSET))

        def _parse_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        text = _parse_text(d.pop("text", UNSET))

        def _parse_total_errors(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_errors = _parse_total_errors(d.pop("total_errors", UNSET))

        def _parse_width(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        width = _parse_width(d.pop("width", UNSET))

        def _parse_wrong_tag(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        wrong_tag = _parse_wrong_tag(d.pop("wrong_tag", UNSET))

        def _parse_x(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        x = _parse_x(d.pop("x", UNSET))

        def _parse_y(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        y = _parse_y(d.pop("y", UNSET))

        data_row = cls(
            id=id,
            background=background,
            bleu=bleu,
            boundary_iou=boundary_iou,
            boxes=boxes,
            classification=classification,
            classification_and_localization=classification_and_localization,
            confidence=confidence,
            data_error_potential=data_error_potential,
            dep_mask=dep_mask,
            drift_score=drift_score,
            duplicate=duplicate,
            edit_relabeled=edit_relabeled,
            edited=edited,
            generated_output=generated_output,
            generated_segments=generated_segments,
            generated_uncertainty=generated_uncertainty,
            ghost_span=ghost_span,
            gold=gold,
            height=height,
            image=image,
            input_=input_,
            input_cutoff=input_cutoff,
            is_drifted=is_drifted,
            is_on_the_boundary=is_on_the_boundary,
            localization=localization,
            max_dep=max_dep,
            max_dep_label=max_dep_label,
            mean_iou=mean_iou,
            meta=meta,
            missed=missed,
            missed_label=missed_label,
            mltc_golds=mltc_golds,
            mltc_golds_deps=mltc_golds_deps,
            mltc_preds=mltc_preds,
            mltc_preds_deps=mltc_preds_deps,
            noise_type=noise_type,
            perplexity=perplexity,
            polygons=polygons,
            pred=pred,
            rouge=rouge,
            span_shift=span_shift,
            spans=spans,
            system_prompts=system_prompts,
            target=target,
            target_cutoff=target_cutoff,
            target_segments=target_segments,
            text=text,
            total_errors=total_errors,
            width=width,
            wrong_tag=wrong_tag,
            x=x,
            y=y,
        )

        data_row.additional_properties = d
        return data_row

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
