from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.content_modality import ContentModality
from ..models.control_applies_to import ControlAppliesTo
from ..models.control_check_stage import ControlCheckStage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.control_result import ControlResult
    from ..models.control_span_record_annotation_aggregates import ControlSpanRecordAnnotationAggregates
    from ..models.control_span_record_annotations import ControlSpanRecordAnnotations
    from ..models.control_span_record_dataset_metadata import ControlSpanRecordDatasetMetadata
    from ..models.control_span_record_feedback_rating_info import ControlSpanRecordFeedbackRatingInfo
    from ..models.control_span_record_user_metadata import ControlSpanRecordUserMetadata
    from ..models.file_content_part import FileContentPart
    from ..models.message import Message
    from ..models.metrics import Metrics
    from ..models.text_content_part import TextContentPart


T = TypeVar("T", bound="ControlSpanRecord")


@_attrs_define
class ControlSpanRecord:
    """
    Attributes:
        id (str): Galileo ID of the session, trace or span
        session_id (str): Galileo ID of the session containing the trace (or the same value as id for a trace)
        project_id (str): Galileo ID of the project associated with this trace or span
        run_id (str): Galileo ID of the run (log stream or experiment) associated with this trace or span
        parent_id (str): Galileo ID of the parent of this span
        type_ (Literal['control'] | Unset): Type of the trace, span or session. Default: 'control'.
        input_ (list[FileContentPart | TextContentPart] | list[Message] | str | Unset): Input to the trace or span.
            Default: ''.
        redacted_input (list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset): Redacted input of
            the trace or span.
        output (ControlResult | None | Unset): Output of the trace or span.
        redacted_output (ControlResult | None | Unset): Redacted output of the trace or span.
        name (str | Unset): Name of the trace, span or session. Default: ''.
        created_at (datetime.datetime | Unset): Timestamp of the trace or span's creation.
        user_metadata (ControlSpanRecordUserMetadata | Unset): Metadata associated with this trace or span.
        tags (list[str] | Unset): Tags associated with this trace or span.
        status_code (int | None | Unset): Status code of the trace or span. Used for logging failure or error states.
        metrics (Metrics | Unset):
        external_id (None | str | Unset): A user-provided session, trace or span ID.
        dataset_input (None | str | Unset): Input to the dataset associated with this trace
        dataset_output (None | str | Unset): Output from the dataset associated with this trace
        dataset_metadata (ControlSpanRecordDatasetMetadata | Unset): Metadata from the dataset associated with this
            trace
        trace_id (None | str | Unset): Galileo ID of the trace containing the span (or the same value as id for a trace)
        updated_at (datetime.datetime | None | Unset): Timestamp of the session or trace or span's last update
        has_children (bool | None | Unset): Whether or not this trace or span has child spans
        metrics_batch_id (None | str | Unset): Galileo ID of the metrics batch associated with this trace or span
        session_batch_id (None | str | Unset): Galileo ID of the metrics batch associated with this trace or span
        feedback_rating_info (ControlSpanRecordFeedbackRatingInfo | Unset): Feedback information related to the record
        annotations (ControlSpanRecordAnnotations | Unset): Annotations keyed by template ID and annotator ID
        file_ids (list[str] | Unset): IDs of files associated with this record
        file_modalities (list[ContentModality] | Unset): Modalities of files associated with this record
        annotation_aggregates (ControlSpanRecordAnnotationAggregates | Unset): Annotation aggregate information keyed by
            template ID
        annotation_queue_ids (list[str] | Unset): IDs of annotation queues this record is in
        is_complete (bool | Unset): Whether the parent trace is complete or not Default: True.
        step_number (int | None | Unset): Topological step number of the span.
        control_id (int | None | Unset): Identifier of the control definition that produced this span.
        agent_name (None | str | Unset): Normalized agent name associated with this control execution.
        check_stage (ControlCheckStage | None | Unset): Execution stage where the control ran, typically 'pre' or
            'post'.
        applies_to (ControlAppliesTo | None | Unset): Parent execution type the control applied to, for example
            'llm_call' or 'tool_call'.
        evaluator_name (None | str | Unset): Representative evaluator name for this control span. For composite
            controls, this is the primary evaluator chosen for observability identity.
        selector_path (None | str | Unset): Representative selector path for this control span. For composite controls,
            this is the primary selector path chosen for observability identity.
    """

    id: str
    session_id: str
    project_id: str
    run_id: str
    parent_id: str
    type_: Literal["control"] | Unset = "control"
    input_: list[FileContentPart | TextContentPart] | list[Message] | str | Unset = ""
    redacted_input: list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset = UNSET
    output: ControlResult | None | Unset = UNSET
    redacted_output: ControlResult | None | Unset = UNSET
    name: str | Unset = ""
    created_at: datetime.datetime | Unset = UNSET
    user_metadata: ControlSpanRecordUserMetadata | Unset = UNSET
    tags: list[str] | Unset = UNSET
    status_code: int | None | Unset = UNSET
    metrics: Metrics | Unset = UNSET
    external_id: None | str | Unset = UNSET
    dataset_input: None | str | Unset = UNSET
    dataset_output: None | str | Unset = UNSET
    dataset_metadata: ControlSpanRecordDatasetMetadata | Unset = UNSET
    trace_id: None | str | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    has_children: bool | None | Unset = UNSET
    metrics_batch_id: None | str | Unset = UNSET
    session_batch_id: None | str | Unset = UNSET
    feedback_rating_info: ControlSpanRecordFeedbackRatingInfo | Unset = UNSET
    annotations: ControlSpanRecordAnnotations | Unset = UNSET
    file_ids: list[str] | Unset = UNSET
    file_modalities: list[ContentModality] | Unset = UNSET
    annotation_aggregates: ControlSpanRecordAnnotationAggregates | Unset = UNSET
    annotation_queue_ids: list[str] | Unset = UNSET
    is_complete: bool | Unset = True
    step_number: int | None | Unset = UNSET
    control_id: int | None | Unset = UNSET
    agent_name: None | str | Unset = UNSET
    check_stage: ControlCheckStage | None | Unset = UNSET
    applies_to: ControlAppliesTo | None | Unset = UNSET
    evaluator_name: None | str | Unset = UNSET
    selector_path: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.control_result import ControlResult
        from ..models.text_content_part import TextContentPart

        id = self.id

        session_id = self.session_id

        project_id = self.project_id

        run_id = self.run_id

        parent_id = self.parent_id

        type_ = self.type_

        input_: list[dict[str, Any]] | str | Unset
        if isinstance(self.input_, Unset):
            input_ = UNSET
        elif isinstance(self.input_, list):
            input_ = []
            for input_type_1_item_data in self.input_:
                input_type_1_item = input_type_1_item_data.to_dict()
                input_.append(input_type_1_item)

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_2_item_data in self.input_:
                input_type_2_item: dict[str, Any]
                if isinstance(input_type_2_item_data, TextContentPart):
                    input_type_2_item = input_type_2_item_data.to_dict()
                else:
                    input_type_2_item = input_type_2_item_data.to_dict()

                input_.append(input_type_2_item)

        else:
            input_ = self.input_

        redacted_input: list[dict[str, Any]] | None | str | Unset
        if isinstance(self.redacted_input, Unset):
            redacted_input = UNSET
        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_1_item_data in self.redacted_input:
                redacted_input_type_1_item = redacted_input_type_1_item_data.to_dict()
                redacted_input.append(redacted_input_type_1_item)

        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_2_item_data in self.redacted_input:
                redacted_input_type_2_item: dict[str, Any]
                if isinstance(redacted_input_type_2_item_data, TextContentPart):
                    redacted_input_type_2_item = redacted_input_type_2_item_data.to_dict()
                else:
                    redacted_input_type_2_item = redacted_input_type_2_item_data.to_dict()

                redacted_input.append(redacted_input_type_2_item)

        else:
            redacted_input = self.redacted_input

        output: dict[str, Any] | None | Unset
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, ControlResult):
            output = self.output.to_dict()
        else:
            output = self.output

        redacted_output: dict[str, Any] | None | Unset
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        elif isinstance(self.redacted_output, ControlResult):
            redacted_output = self.redacted_output.to_dict()
        else:
            redacted_output = self.redacted_output

        name = self.name

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        user_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        status_code: int | None | Unset
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        metrics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        external_id: None | str | Unset
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        dataset_input: None | str | Unset
        if isinstance(self.dataset_input, Unset):
            dataset_input = UNSET
        else:
            dataset_input = self.dataset_input

        dataset_output: None | str | Unset
        if isinstance(self.dataset_output, Unset):
            dataset_output = UNSET
        else:
            dataset_output = self.dataset_output

        dataset_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dataset_metadata, Unset):
            dataset_metadata = self.dataset_metadata.to_dict()

        trace_id: None | str | Unset
        if isinstance(self.trace_id, Unset):
            trace_id = UNSET
        else:
            trace_id = self.trace_id

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        has_children: bool | None | Unset
        if isinstance(self.has_children, Unset):
            has_children = UNSET
        else:
            has_children = self.has_children

        metrics_batch_id: None | str | Unset
        if isinstance(self.metrics_batch_id, Unset):
            metrics_batch_id = UNSET
        else:
            metrics_batch_id = self.metrics_batch_id

        session_batch_id: None | str | Unset
        if isinstance(self.session_batch_id, Unset):
            session_batch_id = UNSET
        else:
            session_batch_id = self.session_batch_id

        feedback_rating_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.feedback_rating_info, Unset):
            feedback_rating_info = self.feedback_rating_info.to_dict()

        annotations: dict[str, Any] | Unset = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = self.annotations.to_dict()

        file_ids: list[str] | Unset = UNSET
        if not isinstance(self.file_ids, Unset):
            file_ids = self.file_ids

        file_modalities: list[str] | Unset = UNSET
        if not isinstance(self.file_modalities, Unset):
            file_modalities = []
            for file_modalities_item_data in self.file_modalities:
                file_modalities_item = file_modalities_item_data.value
                file_modalities.append(file_modalities_item)

        annotation_aggregates: dict[str, Any] | Unset = UNSET
        if not isinstance(self.annotation_aggregates, Unset):
            annotation_aggregates = self.annotation_aggregates.to_dict()

        annotation_queue_ids: list[str] | Unset = UNSET
        if not isinstance(self.annotation_queue_ids, Unset):
            annotation_queue_ids = self.annotation_queue_ids

        is_complete = self.is_complete

        step_number: int | None | Unset
        if isinstance(self.step_number, Unset):
            step_number = UNSET
        else:
            step_number = self.step_number

        control_id: int | None | Unset
        if isinstance(self.control_id, Unset):
            control_id = UNSET
        else:
            control_id = self.control_id

        agent_name: None | str | Unset
        if isinstance(self.agent_name, Unset):
            agent_name = UNSET
        else:
            agent_name = self.agent_name

        check_stage: None | str | Unset
        if isinstance(self.check_stage, Unset):
            check_stage = UNSET
        elif isinstance(self.check_stage, ControlCheckStage):
            check_stage = self.check_stage.value
        else:
            check_stage = self.check_stage

        applies_to: None | str | Unset
        if isinstance(self.applies_to, Unset):
            applies_to = UNSET
        elif isinstance(self.applies_to, ControlAppliesTo):
            applies_to = self.applies_to.value
        else:
            applies_to = self.applies_to

        evaluator_name: None | str | Unset
        if isinstance(self.evaluator_name, Unset):
            evaluator_name = UNSET
        else:
            evaluator_name = self.evaluator_name

        selector_path: None | str | Unset
        if isinstance(self.selector_path, Unset):
            selector_path = UNSET
        else:
            selector_path = self.selector_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "session_id": session_id, "project_id": project_id, "run_id": run_id, "parent_id": parent_id}
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if input_ is not UNSET:
            field_dict["input"] = input_
        if redacted_input is not UNSET:
            field_dict["redacted_input"] = redacted_input
        if output is not UNSET:
            field_dict["output"] = output
        if redacted_output is not UNSET:
            field_dict["redacted_output"] = redacted_output
        if name is not UNSET:
            field_dict["name"] = name
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata
        if tags is not UNSET:
            field_dict["tags"] = tags
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if dataset_input is not UNSET:
            field_dict["dataset_input"] = dataset_input
        if dataset_output is not UNSET:
            field_dict["dataset_output"] = dataset_output
        if dataset_metadata is not UNSET:
            field_dict["dataset_metadata"] = dataset_metadata
        if trace_id is not UNSET:
            field_dict["trace_id"] = trace_id
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if has_children is not UNSET:
            field_dict["has_children"] = has_children
        if metrics_batch_id is not UNSET:
            field_dict["metrics_batch_id"] = metrics_batch_id
        if session_batch_id is not UNSET:
            field_dict["session_batch_id"] = session_batch_id
        if feedback_rating_info is not UNSET:
            field_dict["feedback_rating_info"] = feedback_rating_info
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if file_ids is not UNSET:
            field_dict["file_ids"] = file_ids
        if file_modalities is not UNSET:
            field_dict["file_modalities"] = file_modalities
        if annotation_aggregates is not UNSET:
            field_dict["annotation_aggregates"] = annotation_aggregates
        if annotation_queue_ids is not UNSET:
            field_dict["annotation_queue_ids"] = annotation_queue_ids
        if is_complete is not UNSET:
            field_dict["is_complete"] = is_complete
        if step_number is not UNSET:
            field_dict["step_number"] = step_number
        if control_id is not UNSET:
            field_dict["control_id"] = control_id
        if agent_name is not UNSET:
            field_dict["agent_name"] = agent_name
        if check_stage is not UNSET:
            field_dict["check_stage"] = check_stage
        if applies_to is not UNSET:
            field_dict["applies_to"] = applies_to
        if evaluator_name is not UNSET:
            field_dict["evaluator_name"] = evaluator_name
        if selector_path is not UNSET:
            field_dict["selector_path"] = selector_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.control_result import ControlResult
        from ..models.control_span_record_annotation_aggregates import ControlSpanRecordAnnotationAggregates
        from ..models.control_span_record_annotations import ControlSpanRecordAnnotations
        from ..models.control_span_record_dataset_metadata import ControlSpanRecordDatasetMetadata
        from ..models.control_span_record_feedback_rating_info import ControlSpanRecordFeedbackRatingInfo
        from ..models.control_span_record_user_metadata import ControlSpanRecordUserMetadata
        from ..models.file_content_part import FileContentPart
        from ..models.message import Message
        from ..models.metrics import Metrics
        from ..models.text_content_part import TextContentPart

        d = dict(src_dict)
        id = d.pop("id")

        session_id = d.pop("session_id")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        parent_id = d.pop("parent_id")

        type_ = cast(Literal["control"] | Unset, d.pop("type", UNSET))
        if type_ != "control" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'control', got '{type_}'")

        def _parse_input_(data: object) -> list[FileContentPart | TextContentPart] | list[Message] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_1 = []
                _input_type_1 = data
                for input_type_1_item_data in _input_type_1:
                    input_type_1_item = Message.from_dict(input_type_1_item_data)

                    input_type_1.append(input_type_1_item)

                return input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_2 = []
                _input_type_2 = data
                for input_type_2_item_data in _input_type_2:

                    def _parse_input_type_2_item(data: object) -> FileContentPart | TextContentPart:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            input_type_2_item_type_0 = TextContentPart.from_dict(data)

                            return input_type_2_item_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        input_type_2_item_type_1 = FileContentPart.from_dict(data)

                        return input_type_2_item_type_1

                    input_type_2_item = _parse_input_type_2_item(input_type_2_item_data)

                    input_type_2.append(input_type_2_item)

                return input_type_2
            except:  # noqa: E722
                pass
            return cast(list[FileContentPart | TextContentPart] | list[Message] | str | Unset, data)

        input_ = _parse_input_(d.pop("input", UNSET))

        def _parse_redacted_input(
            data: object,
        ) -> list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_1 = []
                _redacted_input_type_1 = data
                for redacted_input_type_1_item_data in _redacted_input_type_1:
                    redacted_input_type_1_item = Message.from_dict(redacted_input_type_1_item_data)

                    redacted_input_type_1.append(redacted_input_type_1_item)

                return redacted_input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_2 = []
                _redacted_input_type_2 = data
                for redacted_input_type_2_item_data in _redacted_input_type_2:

                    def _parse_redacted_input_type_2_item(data: object) -> FileContentPart | TextContentPart:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            redacted_input_type_2_item_type_0 = TextContentPart.from_dict(data)

                            return redacted_input_type_2_item_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        redacted_input_type_2_item_type_1 = FileContentPart.from_dict(data)

                        return redacted_input_type_2_item_type_1

                    redacted_input_type_2_item = _parse_redacted_input_type_2_item(redacted_input_type_2_item_data)

                    redacted_input_type_2.append(redacted_input_type_2_item)

                return redacted_input_type_2
            except:  # noqa: E722
                pass
            return cast(list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset, data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        def _parse_output(data: object) -> ControlResult | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_0 = ControlResult.from_dict(data)

                return output_type_0
            except:  # noqa: E722
                pass
            return cast(ControlResult | None | Unset, data)

        output = _parse_output(d.pop("output", UNSET))

        def _parse_redacted_output(data: object) -> ControlResult | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_output_type_0 = ControlResult.from_dict(data)

                return redacted_output_type_0
            except:  # noqa: E722
                pass
            return cast(ControlResult | None | Unset, data)

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: ControlSpanRecordUserMetadata | Unset
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = ControlSpanRecordUserMetadata.from_dict(_user_metadata)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_status_code(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Metrics | Unset
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = Metrics.from_dict(_metrics)

        def _parse_external_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_dataset_input(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_input = _parse_dataset_input(d.pop("dataset_input", UNSET))

        def _parse_dataset_output(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_output = _parse_dataset_output(d.pop("dataset_output", UNSET))

        _dataset_metadata = d.pop("dataset_metadata", UNSET)
        dataset_metadata: ControlSpanRecordDatasetMetadata | Unset
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = ControlSpanRecordDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_trace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trace_id = _parse_trace_id(d.pop("trace_id", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_has_children(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        has_children = _parse_has_children(d.pop("has_children", UNSET))

        def _parse_metrics_batch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metrics_batch_id = _parse_metrics_batch_id(d.pop("metrics_batch_id", UNSET))

        def _parse_session_batch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_batch_id = _parse_session_batch_id(d.pop("session_batch_id", UNSET))

        _feedback_rating_info = d.pop("feedback_rating_info", UNSET)
        feedback_rating_info: ControlSpanRecordFeedbackRatingInfo | Unset
        if isinstance(_feedback_rating_info, Unset):
            feedback_rating_info = UNSET
        else:
            feedback_rating_info = ControlSpanRecordFeedbackRatingInfo.from_dict(_feedback_rating_info)

        _annotations = d.pop("annotations", UNSET)
        annotations: ControlSpanRecordAnnotations | Unset
        if isinstance(_annotations, Unset):
            annotations = UNSET
        else:
            annotations = ControlSpanRecordAnnotations.from_dict(_annotations)

        file_ids = cast(list[str], d.pop("file_ids", UNSET))

        _file_modalities = d.pop("file_modalities", UNSET)
        file_modalities: list[ContentModality] | Unset = UNSET
        if _file_modalities is not UNSET:
            file_modalities = []
            for file_modalities_item_data in _file_modalities:
                file_modalities_item = ContentModality(file_modalities_item_data)

                file_modalities.append(file_modalities_item)

        _annotation_aggregates = d.pop("annotation_aggregates", UNSET)
        annotation_aggregates: ControlSpanRecordAnnotationAggregates | Unset
        if isinstance(_annotation_aggregates, Unset):
            annotation_aggregates = UNSET
        else:
            annotation_aggregates = ControlSpanRecordAnnotationAggregates.from_dict(_annotation_aggregates)

        annotation_queue_ids = cast(list[str], d.pop("annotation_queue_ids", UNSET))

        is_complete = d.pop("is_complete", UNSET)

        def _parse_step_number(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        step_number = _parse_step_number(d.pop("step_number", UNSET))

        def _parse_control_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        control_id = _parse_control_id(d.pop("control_id", UNSET))

        def _parse_agent_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_name = _parse_agent_name(d.pop("agent_name", UNSET))

        def _parse_check_stage(data: object) -> ControlCheckStage | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                check_stage_type_0 = ControlCheckStage(data)

                return check_stage_type_0
            except:  # noqa: E722
                pass
            return cast(ControlCheckStage | None | Unset, data)

        check_stage = _parse_check_stage(d.pop("check_stage", UNSET))

        def _parse_applies_to(data: object) -> ControlAppliesTo | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                applies_to_type_0 = ControlAppliesTo(data)

                return applies_to_type_0
            except:  # noqa: E722
                pass
            return cast(ControlAppliesTo | None | Unset, data)

        applies_to = _parse_applies_to(d.pop("applies_to", UNSET))

        def _parse_evaluator_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        evaluator_name = _parse_evaluator_name(d.pop("evaluator_name", UNSET))

        def _parse_selector_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        selector_path = _parse_selector_path(d.pop("selector_path", UNSET))

        control_span_record = cls(
            id=id,
            session_id=session_id,
            project_id=project_id,
            run_id=run_id,
            parent_id=parent_id,
            type_=type_,
            input_=input_,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=created_at,
            user_metadata=user_metadata,
            tags=tags,
            status_code=status_code,
            metrics=metrics,
            external_id=external_id,
            dataset_input=dataset_input,
            dataset_output=dataset_output,
            dataset_metadata=dataset_metadata,
            trace_id=trace_id,
            updated_at=updated_at,
            has_children=has_children,
            metrics_batch_id=metrics_batch_id,
            session_batch_id=session_batch_id,
            feedback_rating_info=feedback_rating_info,
            annotations=annotations,
            file_ids=file_ids,
            file_modalities=file_modalities,
            annotation_aggregates=annotation_aggregates,
            annotation_queue_ids=annotation_queue_ids,
            is_complete=is_complete,
            step_number=step_number,
            control_id=control_id,
            agent_name=agent_name,
            check_stage=check_stage,
            applies_to=applies_to,
            evaluator_name=evaluator_name,
            selector_path=selector_path,
        )

        control_span_record.additional_properties = d
        return control_span_record

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
