from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.control_action import ControlAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="ControlResult")


@_attrs_define
class ControlResult:
    """
    Attributes
    ----------
        action (ControlAction):
        matched (bool): Whether the control matched. False covers both non-match and error cases; use error_message to
            distinguish errors.
        confidence (float | None | Unset): Confidence score reported by the control evaluation result.
        error_message (None | str | Unset): Error text when control evaluation failed. This should be null for normal
            matches and non-matches.
    """

    action: ControlAction
    matched: bool
    confidence: float | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        matched = self.matched

        confidence: float | None | Unset
        confidence = UNSET if isinstance(self.confidence, Unset) else self.confidence

        error_message: None | str | Unset
        error_message = UNSET if isinstance(self.error_message, Unset) else self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"action": action, "matched": matched})
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = ControlAction(d.pop("action"))

        matched = d.pop("matched")

        def _parse_confidence(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        control_result = cls(action=action, matched=matched, confidence=confidence, error_message=error_message)

        control_result.additional_properties = d
        return control_result

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
