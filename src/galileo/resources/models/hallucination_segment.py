from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HallucinationSegment")


@_attrs_define
class HallucinationSegment:
    """
    Attributes
    ----------
        start (int):
        end (int):
        hallucination (float):
        hallucination_severity (Union[Unset, int]):  Default: 0.
    """

    start: int
    end: int
    hallucination: float
    hallucination_severity: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start = self.start

        end = self.end

        hallucination = self.hallucination

        hallucination_severity = self.hallucination_severity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"start": start, "end": end, "hallucination": hallucination})
        if hallucination_severity is not UNSET:
            field_dict["hallucination_severity"] = hallucination_severity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start = d.pop("start")

        end = d.pop("end")

        hallucination = d.pop("hallucination")

        hallucination_severity = d.pop("hallucination_severity", UNSET)

        hallucination_segment = cls(
            start=start, end=end, hallucination=hallucination, hallucination_severity=hallucination_severity
        )

        hallucination_segment.additional_properties = d
        return hallucination_segment

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
