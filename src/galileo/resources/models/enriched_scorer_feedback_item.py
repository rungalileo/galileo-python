from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EnrichedScorerFeedbackItem")


@_attrs_define
class EnrichedScorerFeedbackItem:
    """Enriched feedback item with record data and entity names.

    Attributes:
        id (str):
        project_id (str):
        run_id (str):
        scorer_id (str):
        source_scorer_version_id (str):
        record_id (str):
        original_value (str):
        annotated_value (str):
        feedback_text (None | str):
        rationale (None | str):
        queue_id (str):
        created_by (None | str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        project_name (str): Name of the project
        run_name (str): Name of the run
        created_by_name (None | str | Unset):
        input_ (None | str | Unset): Input data for the record that was scored
        output (None | str | Unset): Output data for the record that was scored
    """

    id: str
    project_id: str
    run_id: str
    scorer_id: str
    source_scorer_version_id: str
    record_id: str
    original_value: str
    annotated_value: str
    feedback_text: None | str
    rationale: None | str
    queue_id: str
    created_by: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    project_name: str
    run_name: str
    created_by_name: None | str | Unset = UNSET
    input_: None | str | Unset = UNSET
    output: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        project_id = self.project_id

        run_id = self.run_id

        scorer_id = self.scorer_id

        source_scorer_version_id = self.source_scorer_version_id

        record_id = self.record_id

        original_value = self.original_value

        annotated_value = self.annotated_value

        feedback_text: None | str
        feedback_text = self.feedback_text

        rationale: None | str
        rationale = self.rationale

        queue_id = self.queue_id

        created_by: None | str
        created_by = self.created_by

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        project_name = self.project_name

        run_name = self.run_name

        created_by_name: None | str | Unset
        if isinstance(self.created_by_name, Unset):
            created_by_name = UNSET
        else:
            created_by_name = self.created_by_name

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "run_id": run_id,
                "scorer_id": scorer_id,
                "source_scorer_version_id": source_scorer_version_id,
                "record_id": record_id,
                "original_value": original_value,
                "annotated_value": annotated_value,
                "feedback_text": feedback_text,
                "rationale": rationale,
                "queue_id": queue_id,
                "created_by": created_by,
                "created_at": created_at,
                "updated_at": updated_at,
                "project_name": project_name,
                "run_name": run_name,
            }
        )
        if created_by_name is not UNSET:
            field_dict["created_by_name"] = created_by_name
        if input_ is not UNSET:
            field_dict["input"] = input_
        if output is not UNSET:
            field_dict["output"] = output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        scorer_id = d.pop("scorer_id")

        source_scorer_version_id = d.pop("source_scorer_version_id")

        record_id = d.pop("record_id")

        original_value = d.pop("original_value")

        annotated_value = d.pop("annotated_value")

        def _parse_feedback_text(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        feedback_text = _parse_feedback_text(d.pop("feedback_text"))

        def _parse_rationale(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        rationale = _parse_rationale(d.pop("rationale"))

        queue_id = d.pop("queue_id")

        def _parse_created_by(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        created_by = _parse_created_by(d.pop("created_by"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        project_name = d.pop("project_name")

        run_name = d.pop("run_name")

        def _parse_created_by_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_by_name = _parse_created_by_name(d.pop("created_by_name", UNSET))

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

        enriched_scorer_feedback_item = cls(
            id=id,
            project_id=project_id,
            run_id=run_id,
            scorer_id=scorer_id,
            source_scorer_version_id=source_scorer_version_id,
            record_id=record_id,
            original_value=original_value,
            annotated_value=annotated_value,
            feedback_text=feedback_text,
            rationale=rationale,
            queue_id=queue_id,
            created_by=created_by,
            created_at=created_at,
            updated_at=updated_at,
            project_name=project_name,
            run_name=run_name,
            created_by_name=created_by_name,
            input_=input_,
            output=output,
        )

        enriched_scorer_feedback_item.additional_properties = d
        return enriched_scorer_feedback_item

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
