from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Segment")


@_attrs_define
class Segment:
    """
    Attributes:
        end (int):
        start (int):
        value (Union[float, int, str]):
        prob (Union[None, Unset, float]):
    """

    end: int
    start: int
    value: Union[float, int, str]
    prob: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        end = self.end

        start = self.start

        value: Union[float, int, str]
        value = self.value

        prob: Union[None, Unset, float]
        if isinstance(self.prob, Unset):
            prob = UNSET
        else:
            prob = self.prob

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"end": end, "start": start, "value": value})
        if prob is not UNSET:
            field_dict["prob"] = prob

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        end = d.pop("end")

        start = d.pop("start")

        def _parse_value(data: object) -> Union[float, int, str]:
            return cast(Union[float, int, str], data)

        value = _parse_value(d.pop("value"))

        def _parse_prob(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        prob = _parse_prob(d.pop("prob", UNSET))

        segment = cls(end=end, start=start, value=value, prob=prob)

        segment.additional_properties = d
        return segment

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
