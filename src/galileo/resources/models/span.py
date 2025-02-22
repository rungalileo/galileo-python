from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Span")


@_attrs_define
class Span:
    """
    Attributes:
        id (int):
        is_active (bool):
        pred (str):
        span_end (int):
        span_start (int):
        confidence (Union[None, Unset, float]):
        data_error_potential (Union[None, Unset, float]):
        error_type (Union[None, Unset, str]):
        gold (Union[None, Unset, str]):
        is_drifted (Union[None, Unset, bool]):
        is_on_the_boundary (Union[None, Unset, bool]):
        x (Union[None, Unset, float]):
        y (Union[None, Unset, float]):
    """

    id: int
    is_active: bool
    pred: str
    span_end: int
    span_start: int
    confidence: Union[None, Unset, float] = UNSET
    data_error_potential: Union[None, Unset, float] = UNSET
    error_type: Union[None, Unset, str] = UNSET
    gold: Union[None, Unset, str] = UNSET
    is_drifted: Union[None, Unset, bool] = UNSET
    is_on_the_boundary: Union[None, Unset, bool] = UNSET
    x: Union[None, Unset, float] = UNSET
    y: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        is_active = self.is_active

        pred = self.pred

        span_end = self.span_end

        span_start = self.span_start

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
        field_dict.update(
            {"id": id, "is_active": is_active, "pred": pred, "span_end": span_end, "span_start": span_start}
        )
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if data_error_potential is not UNSET:
            field_dict["data_error_potential"] = data_error_potential
        if error_type is not UNSET:
            field_dict["error_type"] = error_type
        if gold is not UNSET:
            field_dict["gold"] = gold
        if is_drifted is not UNSET:
            field_dict["is_drifted"] = is_drifted
        if is_on_the_boundary is not UNSET:
            field_dict["is_on_the_boundary"] = is_on_the_boundary
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        is_active = d.pop("is_active")

        pred = d.pop("pred")

        span_end = d.pop("span_end")

        span_start = d.pop("span_start")

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

        span = cls(
            id=id,
            is_active=is_active,
            pred=pred,
            span_end=span_end,
            span_start=span_start,
            confidence=confidence,
            data_error_potential=data_error_potential,
            error_type=error_type,
            gold=gold,
            is_drifted=is_drifted,
            is_on_the_boundary=is_on_the_boundary,
            x=x,
            y=y,
        )

        span.additional_properties = d
        return span

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
