from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateScorerFeedbackRequest")


@_attrs_define
class CreateScorerFeedbackRequest:
    """Request schema for creating scorer feedback.

    Attributes:
        project_id (str): Project context for audit trail
        run_id (str): Run context
        scorer_id (str): Scorer being corrected
        scorer_version_id (str): Version that produced the incorrect output
        record_id (str): ID of the record that was scored
        original_value (str): The original incorrect scorer output
        annotated_value (str): Corrected value (validated against scorer output_type)
        feedback_text (None | str | Unset): Rationale/explanation for the correction
        rationale (None | str | Unset): Original scorer response (value + rationale) for CLHF context
    """

    project_id: str
    run_id: str
    scorer_id: str
    scorer_version_id: str
    record_id: str
    original_value: str
    annotated_value: str
    feedback_text: None | str | Unset = UNSET
    rationale: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        run_id = self.run_id

        scorer_id = self.scorer_id

        scorer_version_id = self.scorer_version_id

        record_id = self.record_id

        original_value = self.original_value

        annotated_value = self.annotated_value

        feedback_text: None | str | Unset
        if isinstance(self.feedback_text, Unset):
            feedback_text = UNSET
        else:
            feedback_text = self.feedback_text

        rationale: None | str | Unset
        if isinstance(self.rationale, Unset):
            rationale = UNSET
        else:
            rationale = self.rationale

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "run_id": run_id,
                "scorer_id": scorer_id,
                "scorer_version_id": scorer_version_id,
                "record_id": record_id,
                "original_value": original_value,
                "annotated_value": annotated_value,
            }
        )
        if feedback_text is not UNSET:
            field_dict["feedback_text"] = feedback_text
        if rationale is not UNSET:
            field_dict["rationale"] = rationale

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        scorer_id = d.pop("scorer_id")

        scorer_version_id = d.pop("scorer_version_id")

        record_id = d.pop("record_id")

        original_value = d.pop("original_value")

        annotated_value = d.pop("annotated_value")

        def _parse_feedback_text(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        feedback_text = _parse_feedback_text(d.pop("feedback_text", UNSET))

        def _parse_rationale(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rationale = _parse_rationale(d.pop("rationale", UNSET))

        create_scorer_feedback_request = cls(
            project_id=project_id,
            run_id=run_id,
            scorer_id=scorer_id,
            scorer_version_id=scorer_version_id,
            record_id=record_id,
            original_value=original_value,
            annotated_value=annotated_value,
            feedback_text=feedback_text,
            rationale=rationale,
        )

        create_scorer_feedback_request.additional_properties = d
        return create_scorer_feedback_request

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
