from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AutotuneValidationResultItem")


@_attrs_define
class AutotuneValidationResultItem:
    """One row in the autotune validation results — one per feedback item.

    Attributes:
        feedback_id (str): Feedback item ID
        record_id (str): Original ClickHouse record ID
        original_value (str): Original scorer output that was incorrect
        annotated_value (str): User-corrected expected value
        input_ (None | str | Unset): Input text of the record
        output (None | str | Unset): Output text of the record
        feedback_text (None | str | Unset): User's explanation for the correction
        new_score (None | str | Unset): New scorer output from the validation run, null if not yet scored
        new_score_rationale (None | str | Unset): Rationale from the new scorer (if CoT enabled), null if not scored or
            CoT disabled
        project_name (None | str | Unset): Name of the source project
        run_name (None | str | Unset): Name of the source run
    """

    feedback_id: str
    record_id: str
    original_value: str
    annotated_value: str
    input_: None | str | Unset = UNSET
    output: None | str | Unset = UNSET
    feedback_text: None | str | Unset = UNSET
    new_score: None | str | Unset = UNSET
    new_score_rationale: None | str | Unset = UNSET
    project_name: None | str | Unset = UNSET
    run_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feedback_id = self.feedback_id

        record_id = self.record_id

        original_value = self.original_value

        annotated_value = self.annotated_value

        input_: None | str | Unset
        if isinstance(self.input_, Unset):
            input_ = UNSET
        else:
            input_ = self.input_

        output: None | str | Unset
        if isinstance(self.output, Unset):
            output = UNSET
        else:
            output = self.output

        feedback_text: None | str | Unset
        if isinstance(self.feedback_text, Unset):
            feedback_text = UNSET
        else:
            feedback_text = self.feedback_text

        new_score: None | str | Unset
        if isinstance(self.new_score, Unset):
            new_score = UNSET
        else:
            new_score = self.new_score

        new_score_rationale: None | str | Unset
        if isinstance(self.new_score_rationale, Unset):
            new_score_rationale = UNSET
        else:
            new_score_rationale = self.new_score_rationale

        project_name: None | str | Unset
        if isinstance(self.project_name, Unset):
            project_name = UNSET
        else:
            project_name = self.project_name

        run_name: None | str | Unset
        if isinstance(self.run_name, Unset):
            run_name = UNSET
        else:
            run_name = self.run_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "feedback_id": feedback_id,
                "record_id": record_id,
                "original_value": original_value,
                "annotated_value": annotated_value,
            }
        )
        if input_ is not UNSET:
            field_dict["input"] = input_
        if output is not UNSET:
            field_dict["output"] = output
        if feedback_text is not UNSET:
            field_dict["feedback_text"] = feedback_text
        if new_score is not UNSET:
            field_dict["new_score"] = new_score
        if new_score_rationale is not UNSET:
            field_dict["new_score_rationale"] = new_score_rationale
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if run_name is not UNSET:
            field_dict["run_name"] = run_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        feedback_id = d.pop("feedback_id")

        record_id = d.pop("record_id")

        original_value = d.pop("original_value")

        annotated_value = d.pop("annotated_value")

        def _parse_input_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        input_ = _parse_input_(d.pop("input", UNSET))

        def _parse_output(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output = _parse_output(d.pop("output", UNSET))

        def _parse_feedback_text(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        feedback_text = _parse_feedback_text(d.pop("feedback_text", UNSET))

        def _parse_new_score(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        new_score = _parse_new_score(d.pop("new_score", UNSET))

        def _parse_new_score_rationale(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        new_score_rationale = _parse_new_score_rationale(d.pop("new_score_rationale", UNSET))

        def _parse_project_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_name = _parse_project_name(d.pop("project_name", UNSET))

        def _parse_run_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        run_name = _parse_run_name(d.pop("run_name", UNSET))

        autotune_validation_result_item = cls(
            feedback_id=feedback_id,
            record_id=record_id,
            original_value=original_value,
            annotated_value=annotated_value,
            input_=input_,
            output=output,
            feedback_text=feedback_text,
            new_score=new_score,
            new_score_rationale=new_score_rationale,
            project_name=project_name,
            run_name=run_name,
        )

        autotune_validation_result_item.additional_properties = d
        return autotune_validation_result_item

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
