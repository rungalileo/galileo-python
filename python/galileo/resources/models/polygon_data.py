from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.polygon_size import PolygonSize
from ..models.sem_seg_error_type import SemSegErrorType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PolygonData")


@_attrs_define
class PolygonData:
    """
    Attributes:
        contours (list[Any]):
        data_error_potential (float):
        id (int):
        is_active (bool):
        is_gold (bool):
        is_pred (bool):
        accuracy (Union[None, Unset, float]):
        area (Union[None, Unset, int]):
        background_error_pct (Union[None, Unset, float]):
        error_type (Union[None, SemSegErrorType, Unset]):
        gold (Union[None, Unset, str]):
        pred (Union[None, Unset, str]):
        size (Union[None, PolygonSize, Unset]):
    """

    contours: list[Any]
    data_error_potential: float
    id: int
    is_active: bool
    is_gold: bool
    is_pred: bool
    accuracy: Union[None, Unset, float] = UNSET
    area: Union[None, Unset, int] = UNSET
    background_error_pct: Union[None, Unset, float] = UNSET
    error_type: Union[None, SemSegErrorType, Unset] = UNSET
    gold: Union[None, Unset, str] = UNSET
    pred: Union[None, Unset, str] = UNSET
    size: Union[None, PolygonSize, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        contours = self.contours

        data_error_potential = self.data_error_potential

        id = self.id

        is_active = self.is_active

        is_gold = self.is_gold

        is_pred = self.is_pred

        accuracy: Union[None, Unset, float]
        if isinstance(self.accuracy, Unset):
            accuracy = UNSET
        else:
            accuracy = self.accuracy

        area: Union[None, Unset, int]
        if isinstance(self.area, Unset):
            area = UNSET
        else:
            area = self.area

        background_error_pct: Union[None, Unset, float]
        if isinstance(self.background_error_pct, Unset):
            background_error_pct = UNSET
        else:
            background_error_pct = self.background_error_pct

        error_type: Union[None, Unset, str]
        if isinstance(self.error_type, Unset):
            error_type = UNSET
        elif isinstance(self.error_type, SemSegErrorType):
            error_type = self.error_type.value
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

        size: Union[None, Unset, str]
        if isinstance(self.size, Unset):
            size = UNSET
        elif isinstance(self.size, PolygonSize):
            size = self.size.value
        else:
            size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "contours": contours,
                "data_error_potential": data_error_potential,
                "id": id,
                "is_active": is_active,
                "is_gold": is_gold,
                "is_pred": is_pred,
            }
        )
        if accuracy is not UNSET:
            field_dict["accuracy"] = accuracy
        if area is not UNSET:
            field_dict["area"] = area
        if background_error_pct is not UNSET:
            field_dict["background_error_pct"] = background_error_pct
        if error_type is not UNSET:
            field_dict["error_type"] = error_type
        if gold is not UNSET:
            field_dict["gold"] = gold
        if pred is not UNSET:
            field_dict["pred"] = pred
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        contours = cast(list[Any], d.pop("contours"))

        data_error_potential = d.pop("data_error_potential")

        id = d.pop("id")

        is_active = d.pop("is_active")

        is_gold = d.pop("is_gold")

        is_pred = d.pop("is_pred")

        def _parse_accuracy(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        accuracy = _parse_accuracy(d.pop("accuracy", UNSET))

        def _parse_area(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        area = _parse_area(d.pop("area", UNSET))

        def _parse_background_error_pct(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        background_error_pct = _parse_background_error_pct(d.pop("background_error_pct", UNSET))

        def _parse_error_type(data: object) -> Union[None, SemSegErrorType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                error_type_type_0 = SemSegErrorType(data)

                return error_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, SemSegErrorType, Unset], data)

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

        def _parse_size(data: object) -> Union[None, PolygonSize, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                size_type_0 = PolygonSize(data)

                return size_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, PolygonSize, Unset], data)

        size = _parse_size(d.pop("size", UNSET))

        polygon_data = cls(
            contours=contours,
            data_error_potential=data_error_potential,
            id=id,
            is_active=is_active,
            is_gold=is_gold,
            is_pred=is_pred,
            accuracy=accuracy,
            area=area,
            background_error_pct=background_error_pct,
            error_type=error_type,
            gold=gold,
            pred=pred,
            size=size,
        )

        polygon_data.additional_properties = d
        return polygon_data

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
