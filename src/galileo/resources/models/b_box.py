from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BBox")


@_attrs_define
class BBox:
    """
    Attributes:
        bbox (list[float]):
        id (int):
        is_active (bool):
        is_gold (bool):
        is_pred (bool):
        confidence (Union[None, Unset, float]):
        data_error_potential (Union[None, Unset, float]):
        error_type (Union[None, Unset, str]):
        gold (Union[None, Unset, str]):
        pred (Union[None, Unset, str]):
        tide_match_id (Union[None, Unset, int]):
        x (Union[None, Unset, float]):
        y (Union[None, Unset, float]):
    """

    bbox: list[float]
    id: int
    is_active: bool
    is_gold: bool
    is_pred: bool
    confidence: Union[None, Unset, float] = UNSET
    data_error_potential: Union[None, Unset, float] = UNSET
    error_type: Union[None, Unset, str] = UNSET
    gold: Union[None, Unset, str] = UNSET
    pred: Union[None, Unset, str] = UNSET
    tide_match_id: Union[None, Unset, int] = UNSET
    x: Union[None, Unset, float] = UNSET
    y: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bbox = self.bbox

        id = self.id

        is_active = self.is_active

        is_gold = self.is_gold

        is_pred = self.is_pred

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

        error_type: Union[None, Unset, str]
        if isinstance(self.error_type, Unset):
            error_type = UNSET
        else:
            error_type = self.error_type

        gold: Union[None, Unset, str]
        if isinstance(self.gold, Unset):
            gold = UNSET
        else:
            gold = self.gold

        pred: Union[None, Unset, str]
        if isinstance(self.pred, Unset):
            pred = UNSET
        else:
            pred = self.pred

        tide_match_id: Union[None, Unset, int]
        if isinstance(self.tide_match_id, Unset):
            tide_match_id = UNSET
        else:
            tide_match_id = self.tide_match_id

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
        field_dict.update({"bbox": bbox, "id": id, "is_active": is_active, "is_gold": is_gold, "is_pred": is_pred})
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if data_error_potential is not UNSET:
            field_dict["data_error_potential"] = data_error_potential
        if error_type is not UNSET:
            field_dict["error_type"] = error_type
        if gold is not UNSET:
            field_dict["gold"] = gold
        if pred is not UNSET:
            field_dict["pred"] = pred
        if tide_match_id is not UNSET:
            field_dict["tide_match_id"] = tide_match_id
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        bbox = cast(list[float], d.pop("bbox"))

        id = d.pop("id")

        is_active = d.pop("is_active")

        is_gold = d.pop("is_gold")

        is_pred = d.pop("is_pred")

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

        def _parse_error_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_type = _parse_error_type(d.pop("error_type", UNSET))

        def _parse_gold(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        gold = _parse_gold(d.pop("gold", UNSET))

        def _parse_pred(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pred = _parse_pred(d.pop("pred", UNSET))

        def _parse_tide_match_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        tide_match_id = _parse_tide_match_id(d.pop("tide_match_id", UNSET))

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

        b_box = cls(
            bbox=bbox,
            id=id,
            is_active=is_active,
            is_gold=is_gold,
            is_pred=is_pred,
            confidence=confidence,
            data_error_potential=data_error_potential,
            error_type=error_type,
            gold=gold,
            pred=pred,
            tide_match_id=tide_match_id,
            x=x,
            y=y,
        )

        b_box.additional_properties = d
        return b_box

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
