from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.b_box import BBox
    from ..models.edit_row_data_meta_type_0 import EditRowDataMetaType0
    from ..models.span import Span


T = TypeVar("T", bound="EditRowData")


@_attrs_define
class EditRowData:
    """
    Attributes:
        generated_output (Union[None, str]):
        id (int):
        input_ (Union[None, str]):
        target (Union[None, str]):
        boxes (Union[None, Unset, list['BBox']]):
        gold (Union[None, Unset, str]):
        image (Union[None, Unset, str]):  Default: ''.
        meta (Union['EditRowDataMetaType0', None, Unset]):
        pred (Union[None, Unset, str]):
        spans (Union[None, Unset, list['Span']]):
        text (Union[None, Unset, str]):
    """

    generated_output: Union[None, str]
    id: int
    input_: Union[None, str]
    target: Union[None, str]
    boxes: Union[None, Unset, list["BBox"]] = UNSET
    gold: Union[None, Unset, str] = UNSET
    image: Union[None, Unset, str] = ""
    meta: Union["EditRowDataMetaType0", None, Unset] = UNSET
    pred: Union[None, Unset, str] = UNSET
    spans: Union[None, Unset, list["Span"]] = UNSET
    text: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.edit_row_data_meta_type_0 import EditRowDataMetaType0

        generated_output: Union[None, str]
        generated_output = self.generated_output

        id = self.id

        input_: Union[None, str]
        input_ = self.input_

        target: Union[None, str]
        target = self.target

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

        meta: Union[None, Unset, dict[str, Any]]
        if isinstance(self.meta, Unset):
            meta = UNSET
        elif isinstance(self.meta, EditRowDataMetaType0):
            meta = self.meta.to_dict()
        else:
            meta = self.meta

        pred: Union[None, Unset, str]
        if isinstance(self.pred, Unset):
            pred = UNSET
        else:
            pred = self.pred

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

        text: Union[None, Unset, str]
        if isinstance(self.text, Unset):
            text = UNSET
        else:
            text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"generated_output": generated_output, "id": id, "input": input_, "target": target})
        if boxes is not UNSET:
            field_dict["boxes"] = boxes
        if gold is not UNSET:
            field_dict["gold"] = gold
        if image is not UNSET:
            field_dict["image"] = image
        if meta is not UNSET:
            field_dict["meta"] = meta
        if pred is not UNSET:
            field_dict["pred"] = pred
        if spans is not UNSET:
            field_dict["spans"] = spans
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.b_box import BBox
        from ..models.edit_row_data_meta_type_0 import EditRowDataMetaType0
        from ..models.span import Span

        d = src_dict.copy()

        def _parse_generated_output(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        generated_output = _parse_generated_output(d.pop("generated_output"))

        id = d.pop("id")

        def _parse_input_(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        input_ = _parse_input_(d.pop("input"))

        def _parse_target(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        target = _parse_target(d.pop("target"))

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

        def _parse_meta(data: object) -> Union["EditRowDataMetaType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                meta_type_0 = EditRowDataMetaType0.from_dict(data)

                return meta_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EditRowDataMetaType0", None, Unset], data)

        meta = _parse_meta(d.pop("meta", UNSET))

        def _parse_pred(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pred = _parse_pred(d.pop("pred", UNSET))

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

        def _parse_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        text = _parse_text(d.pop("text", UNSET))

        edit_row_data = cls(
            generated_output=generated_output,
            id=id,
            input_=input_,
            target=target,
            boxes=boxes,
            gold=gold,
            image=image,
            meta=meta,
            pred=pred,
            spans=spans,
            text=text,
        )

        edit_row_data.additional_properties = d
        return edit_row_data

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
