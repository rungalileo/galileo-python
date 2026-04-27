from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateScorerFeedbackRequest")


@_attrs_define
class UpdateScorerFeedbackRequest:
    """Request schema for updating scorer feedback.

    Attributes:
        annotated_value (None | str | Unset): Updated correct value
        feedback_text (None | str | Unset): Updated explanation (empty string or null clears)
    """

    annotated_value: None | str | Unset = UNSET
    feedback_text: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        annotated_value: None | str | Unset
        if isinstance(self.annotated_value, Unset):
            annotated_value = UNSET
        else:
            annotated_value = self.annotated_value

        feedback_text: None | str | Unset
        if isinstance(self.feedback_text, Unset):
            feedback_text = UNSET
        else:
            feedback_text = self.feedback_text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if annotated_value is not UNSET:
            field_dict["annotated_value"] = annotated_value
        if feedback_text is not UNSET:
            field_dict["feedback_text"] = feedback_text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_annotated_value(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        annotated_value = _parse_annotated_value(d.pop("annotated_value", UNSET))

        def _parse_feedback_text(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        feedback_text = _parse_feedback_text(d.pop("feedback_text", UNSET))

        update_scorer_feedback_request = cls(annotated_value=annotated_value, feedback_text=feedback_text)

        update_scorer_feedback_request.additional_properties = d
        return update_scorer_feedback_request

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
