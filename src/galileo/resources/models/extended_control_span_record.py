import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.content_modality import ContentModality
from ..models.control_applies_to import ControlAppliesTo
from ..models.control_check_stage import ControlCheckStage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.control_result import ControlResult
    from ..models.extended_control_span_record_annotation_aggregates import (
        ExtendedControlSpanRecordAnnotationAggregates,
    )
    from ..models.extended_control_span_record_annotations import ExtendedControlSpanRecordAnnotations
    from ..models.extended_control_span_record_dataset_metadata import ExtendedControlSpanRecordDatasetMetadata
    from ..models.extended_control_span_record_feedback_rating_info import ExtendedControlSpanRecordFeedbackRatingInfo
    from ..models.extended_control_span_record_files_type_0 import ExtendedControlSpanRecordFilesType0
    from ..models.extended_control_span_record_metric_info_type_0 import ExtendedControlSpanRecordMetricInfoType0
    from ..models.extended_control_span_record_user_metadata import ExtendedControlSpanRecordUserMetadata
    from ..models.file_content_part import FileContentPart
    from ..models.message import Message
    from ..models.metrics import Metrics
    from ..models.text_content_part import TextContentPart


T = TypeVar("T", bound="ExtendedControlSpanRecord")


@_attrs_define
class ExtendedControlSpanRecord:
    """
    Attributes
    ----------
        id (str): Galileo ID of the session, trace or span
        session_id (str): Galileo ID of the session containing the trace (or the same value as id for a trace)
        project_id (str): Galileo ID of the project associated with this trace or span
        run_id (str): Galileo ID of the run (log stream or experiment) associated with this trace or span
        parent_id (str): Galileo ID of the parent of this span
        type_ (Union[Literal['control'], Unset]): Type of the trace, span or session. Default: 'control'.
        input_ (Union[Unset, list['Message'], list[Union['FileContentPart', 'TextContentPart']], str]): Input to the
            trace or span. Default: ''.
        redacted_input (Union[None, Unset, list['Message'], list[Union['FileContentPart', 'TextContentPart']], str]):
            Redacted input of the trace or span.
        output (Union['ControlResult', None, Unset]): Output of the trace or span.
        redacted_output (Union['ControlResult', None, Unset]): Redacted output of the trace or span.
        name (Union[Unset, str]): Name of the trace, span or session. Default: ''.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        user_metadata (Union[Unset, ExtendedControlSpanRecordUserMetadata]): Metadata associated with this trace or
            span.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        metrics (Union[Unset, Metrics]):
        external_id (Union[None, Unset, str]): A user-provided session, trace or span ID.
        dataset_input (Union[None, Unset, str]): Input to the dataset associated with this trace
        dataset_output (Union[None, Unset, str]): Output from the dataset associated with this trace
        dataset_metadata (Union[Unset, ExtendedControlSpanRecordDatasetMetadata]): Metadata from the dataset associated
            with this trace
        trace_id (Union[None, Unset, str]): Galileo ID of the trace containing the span (or the same value as id for a
            trace)
        updated_at (Union[None, Unset, datetime.datetime]): Timestamp of the session or trace or span's last update
        has_children (Union[None, Unset, bool]): Whether or not this trace or span has child spans
        metrics_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        session_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        feedback_rating_info (Union[Unset, ExtendedControlSpanRecordFeedbackRatingInfo]): Feedback information related
            to the record
        annotations (Union[Unset, ExtendedControlSpanRecordAnnotations]): Annotations keyed by template ID and annotator
            ID
        file_ids (Union[Unset, list[str]]): IDs of files associated with this record
        file_modalities (Union[Unset, list[ContentModality]]): Modalities of files associated with this record
        annotation_aggregates (Union[Unset, ExtendedControlSpanRecordAnnotationAggregates]): Annotation aggregate
            information keyed by template ID
        annotation_queue_ids (Union[Unset, list[str]]): IDs of annotation queues this record is in
        metric_info (Union['ExtendedControlSpanRecordMetricInfoType0', None, Unset]): Detailed information about the
            metrics associated with this trace or span
        files (Union['ExtendedControlSpanRecordFilesType0', None, Unset]): File metadata keyed by file ID for files
            associated with this record
        is_complete (Union[Unset, bool]): Whether the parent trace is complete or not Default: True.
        step_number (Union[None, Unset, int]): Topological step number of the span.
        control_id (Union[None, Unset, int]): Identifier of the control definition that produced this span.
        agent_name (Union[None, Unset, str]): Normalized agent name associated with this control execution.
        check_stage (Union[ControlCheckStage, None, Unset]): Execution stage where the control ran, typically 'pre' or
            'post'.
        applies_to (Union[ControlAppliesTo, None, Unset]): Parent execution type the control applied to, for example
            'llm_call' or 'tool_call'.
        evaluator_name (Union[None, Unset, str]): Representative evaluator name for this control span. For composite
            controls, this is the primary evaluator chosen for observability identity.
        selector_path (Union[None, Unset, str]): Representative selector path for this control span. For composite
            controls, this is the primary selector path chosen for observability identity.
    """

    id: str
    session_id: str
    project_id: str
    run_id: str
    parent_id: str
    type_: Literal["control"] | Unset = "control"
    input_: Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str = ""
    redacted_input: None | Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str = UNSET
    output: Union["ControlResult", None, Unset] = UNSET
    redacted_output: Union["ControlResult", None, Unset] = UNSET
    name: Unset | str = ""
    created_at: Unset | datetime.datetime = UNSET
    user_metadata: Union[Unset, "ExtendedControlSpanRecordUserMetadata"] = UNSET
    tags: Unset | list[str] = UNSET
    status_code: None | Unset | int = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    external_id: None | Unset | str = UNSET
    dataset_input: None | Unset | str = UNSET
    dataset_output: None | Unset | str = UNSET
    dataset_metadata: Union[Unset, "ExtendedControlSpanRecordDatasetMetadata"] = UNSET
    trace_id: None | Unset | str = UNSET
    updated_at: None | Unset | datetime.datetime = UNSET
    has_children: None | Unset | bool = UNSET
    metrics_batch_id: None | Unset | str = UNSET
    session_batch_id: None | Unset | str = UNSET
    feedback_rating_info: Union[Unset, "ExtendedControlSpanRecordFeedbackRatingInfo"] = UNSET
    annotations: Union[Unset, "ExtendedControlSpanRecordAnnotations"] = UNSET
    file_ids: Unset | list[str] = UNSET
    file_modalities: Unset | list[ContentModality] = UNSET
    annotation_aggregates: Union[Unset, "ExtendedControlSpanRecordAnnotationAggregates"] = UNSET
    annotation_queue_ids: Unset | list[str] = UNSET
    metric_info: Union["ExtendedControlSpanRecordMetricInfoType0", None, Unset] = UNSET
    files: Union["ExtendedControlSpanRecordFilesType0", None, Unset] = UNSET
    is_complete: Unset | bool = True
    step_number: None | Unset | int = UNSET
    control_id: None | Unset | int = UNSET
    agent_name: None | Unset | str = UNSET
    check_stage: ControlCheckStage | None | Unset = UNSET
    applies_to: ControlAppliesTo | None | Unset = UNSET
    evaluator_name: None | Unset | str = UNSET
    selector_path: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.control_result import ControlResult
        from ..models.extended_control_span_record_files_type_0 import ExtendedControlSpanRecordFilesType0
        from ..models.extended_control_span_record_metric_info_type_0 import ExtendedControlSpanRecordMetricInfoType0
        from ..models.text_content_part import TextContentPart

        id = self.id

        session_id = self.session_id

        project_id = self.project_id

        run_id = self.run_id

        parent_id = self.parent_id

        type_ = self.type_

        input_: Unset | list[dict[str, Any]] | str
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

        redacted_input: None | Unset | list[dict[str, Any]] | str
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

        output: None | Unset | dict[str, Any]
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, ControlResult):
            output = self.output.to_dict()
        else:
            output = self.output

        redacted_output: None | Unset | dict[str, Any]
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        elif isinstance(self.redacted_output, ControlResult):
            redacted_output = self.redacted_output.to_dict()
        else:
            redacted_output = self.redacted_output

        name = self.name

        created_at: Unset | str = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        user_metadata: Unset | dict[str, Any] = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        tags: Unset | list[str] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        status_code: None | Unset | int
        status_code = UNSET if isinstance(self.status_code, Unset) else self.status_code

        metrics: Unset | dict[str, Any] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        external_id: None | Unset | str
        external_id = UNSET if isinstance(self.external_id, Unset) else self.external_id

        dataset_input: None | Unset | str
        dataset_input = UNSET if isinstance(self.dataset_input, Unset) else self.dataset_input

        dataset_output: None | Unset | str
        dataset_output = UNSET if isinstance(self.dataset_output, Unset) else self.dataset_output

        dataset_metadata: Unset | dict[str, Any] = UNSET
        if not isinstance(self.dataset_metadata, Unset):
            dataset_metadata = self.dataset_metadata.to_dict()

        trace_id: None | Unset | str
        trace_id = UNSET if isinstance(self.trace_id, Unset) else self.trace_id

        updated_at: None | Unset | str
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        has_children: None | Unset | bool
        has_children = UNSET if isinstance(self.has_children, Unset) else self.has_children

        metrics_batch_id: None | Unset | str
        metrics_batch_id = UNSET if isinstance(self.metrics_batch_id, Unset) else self.metrics_batch_id

        session_batch_id: None | Unset | str
        session_batch_id = UNSET if isinstance(self.session_batch_id, Unset) else self.session_batch_id

        feedback_rating_info: Unset | dict[str, Any] = UNSET
        if not isinstance(self.feedback_rating_info, Unset):
            feedback_rating_info = self.feedback_rating_info.to_dict()

        annotations: Unset | dict[str, Any] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = self.annotations.to_dict()

        file_ids: Unset | list[str] = UNSET
        if not isinstance(self.file_ids, Unset):
            file_ids = self.file_ids

        file_modalities: Unset | list[str] = UNSET
        if not isinstance(self.file_modalities, Unset):
            file_modalities = []
            for file_modalities_item_data in self.file_modalities:
                file_modalities_item = file_modalities_item_data.value
                file_modalities.append(file_modalities_item)

        annotation_aggregates: Unset | dict[str, Any] = UNSET
        if not isinstance(self.annotation_aggregates, Unset):
            annotation_aggregates = self.annotation_aggregates.to_dict()

        annotation_queue_ids: Unset | list[str] = UNSET
        if not isinstance(self.annotation_queue_ids, Unset):
            annotation_queue_ids = self.annotation_queue_ids

        metric_info: None | Unset | dict[str, Any]
        if isinstance(self.metric_info, Unset):
            metric_info = UNSET
        elif isinstance(self.metric_info, ExtendedControlSpanRecordMetricInfoType0):
            metric_info = self.metric_info.to_dict()
        else:
            metric_info = self.metric_info

        files: None | Unset | dict[str, Any]
        if isinstance(self.files, Unset):
            files = UNSET
        elif isinstance(self.files, ExtendedControlSpanRecordFilesType0):
            files = self.files.to_dict()
        else:
            files = self.files

        is_complete = self.is_complete

        step_number: None | Unset | int
        step_number = UNSET if isinstance(self.step_number, Unset) else self.step_number

        control_id: None | Unset | int
        control_id = UNSET if isinstance(self.control_id, Unset) else self.control_id

        agent_name: None | Unset | str
        agent_name = UNSET if isinstance(self.agent_name, Unset) else self.agent_name

        check_stage: None | Unset | str
        if isinstance(self.check_stage, Unset):
            check_stage = UNSET
        elif isinstance(self.check_stage, ControlCheckStage):
            check_stage = self.check_stage.value
        else:
            check_stage = self.check_stage

        applies_to: None | Unset | str
        if isinstance(self.applies_to, Unset):
            applies_to = UNSET
        elif isinstance(self.applies_to, ControlAppliesTo):
            applies_to = self.applies_to.value
        else:
            applies_to = self.applies_to

        evaluator_name: None | Unset | str
        evaluator_name = UNSET if isinstance(self.evaluator_name, Unset) else self.evaluator_name

        selector_path: None | Unset | str
        selector_path = UNSET if isinstance(self.selector_path, Unset) else self.selector_path

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
        if metric_info is not UNSET:
            field_dict["metric_info"] = metric_info
        if files is not UNSET:
            field_dict["files"] = files
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
        from ..models.extended_control_span_record_annotation_aggregates import (
            ExtendedControlSpanRecordAnnotationAggregates,
        )
        from ..models.extended_control_span_record_annotations import ExtendedControlSpanRecordAnnotations
        from ..models.extended_control_span_record_dataset_metadata import ExtendedControlSpanRecordDatasetMetadata
        from ..models.extended_control_span_record_feedback_rating_info import (
            ExtendedControlSpanRecordFeedbackRatingInfo,
        )
        from ..models.extended_control_span_record_files_type_0 import ExtendedControlSpanRecordFilesType0
        from ..models.extended_control_span_record_metric_info_type_0 import ExtendedControlSpanRecordMetricInfoType0
        from ..models.extended_control_span_record_user_metadata import ExtendedControlSpanRecordUserMetadata
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

        def _parse_input_(
            data: object,
        ) -> Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str:
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

                    def _parse_input_type_2_item(data: object) -> Union["FileContentPart", "TextContentPart"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return TextContentPart.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return FileContentPart.from_dict(data)

                    input_type_2_item = _parse_input_type_2_item(input_type_2_item_data)

                    input_type_2.append(input_type_2_item)

                return input_type_2
            except:  # noqa: E722
                pass
            return cast(Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str, data)

        input_ = _parse_input_(d.pop("input", UNSET))

        def _parse_redacted_input(
            data: object,
        ) -> None | Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str:
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

                    def _parse_redacted_input_type_2_item(data: object) -> Union["FileContentPart", "TextContentPart"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return TextContentPart.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return FileContentPart.from_dict(data)

                    redacted_input_type_2_item = _parse_redacted_input_type_2_item(redacted_input_type_2_item_data)

                    redacted_input_type_2.append(redacted_input_type_2_item)

                return redacted_input_type_2
            except:  # noqa: E722
                pass
            return cast(None | Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str, data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        def _parse_output(data: object) -> Union["ControlResult", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ControlResult.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ControlResult", None, Unset], data)

        output = _parse_output(d.pop("output", UNSET))

        def _parse_redacted_output(data: object) -> Union["ControlResult", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ControlResult.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ControlResult", None, Unset], data)

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Unset | datetime.datetime
        created_at = UNSET if isinstance(_created_at, Unset) else isoparse(_created_at)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Unset | ExtendedControlSpanRecordUserMetadata
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = ExtendedControlSpanRecordUserMetadata.from_dict(_user_metadata)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_status_code(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Unset | Metrics
        metrics = UNSET if isinstance(_metrics, Unset) else Metrics.from_dict(_metrics)

        def _parse_external_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_dataset_input(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        dataset_input = _parse_dataset_input(d.pop("dataset_input", UNSET))

        def _parse_dataset_output(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        dataset_output = _parse_dataset_output(d.pop("dataset_output", UNSET))

        _dataset_metadata = d.pop("dataset_metadata", UNSET)
        dataset_metadata: Unset | ExtendedControlSpanRecordDatasetMetadata
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = ExtendedControlSpanRecordDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_trace_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        trace_id = _parse_trace_id(d.pop("trace_id", UNSET))

        def _parse_updated_at(data: object) -> None | Unset | datetime.datetime:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return isoparse(data)

            except:  # noqa: E722
                pass
            return cast(None | Unset | datetime.datetime, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_has_children(data: object) -> None | Unset | bool:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | bool, data)

        has_children = _parse_has_children(d.pop("has_children", UNSET))

        def _parse_metrics_batch_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        metrics_batch_id = _parse_metrics_batch_id(d.pop("metrics_batch_id", UNSET))

        def _parse_session_batch_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        session_batch_id = _parse_session_batch_id(d.pop("session_batch_id", UNSET))

        _feedback_rating_info = d.pop("feedback_rating_info", UNSET)
        feedback_rating_info: Unset | ExtendedControlSpanRecordFeedbackRatingInfo
        if isinstance(_feedback_rating_info, Unset):
            feedback_rating_info = UNSET
        else:
            feedback_rating_info = ExtendedControlSpanRecordFeedbackRatingInfo.from_dict(_feedback_rating_info)

        _annotations = d.pop("annotations", UNSET)
        annotations: Unset | ExtendedControlSpanRecordAnnotations
        if isinstance(_annotations, Unset):
            annotations = UNSET
        else:
            annotations = ExtendedControlSpanRecordAnnotations.from_dict(_annotations)

        file_ids = cast(list[str], d.pop("file_ids", UNSET))

        file_modalities = []
        _file_modalities = d.pop("file_modalities", UNSET)
        for file_modalities_item_data in _file_modalities or []:
            file_modalities_item = ContentModality(file_modalities_item_data)

            file_modalities.append(file_modalities_item)

        _annotation_aggregates = d.pop("annotation_aggregates", UNSET)
        annotation_aggregates: Unset | ExtendedControlSpanRecordAnnotationAggregates
        if isinstance(_annotation_aggregates, Unset):
            annotation_aggregates = UNSET
        else:
            annotation_aggregates = ExtendedControlSpanRecordAnnotationAggregates.from_dict(_annotation_aggregates)

        annotation_queue_ids = cast(list[str], d.pop("annotation_queue_ids", UNSET))

        def _parse_metric_info(data: object) -> Union["ExtendedControlSpanRecordMetricInfoType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExtendedControlSpanRecordMetricInfoType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ExtendedControlSpanRecordMetricInfoType0", None, Unset], data)

        metric_info = _parse_metric_info(d.pop("metric_info", UNSET))

        def _parse_files(data: object) -> Union["ExtendedControlSpanRecordFilesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExtendedControlSpanRecordFilesType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ExtendedControlSpanRecordFilesType0", None, Unset], data)

        files = _parse_files(d.pop("files", UNSET))

        is_complete = d.pop("is_complete", UNSET)

        def _parse_step_number(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        step_number = _parse_step_number(d.pop("step_number", UNSET))

        def _parse_control_id(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        control_id = _parse_control_id(d.pop("control_id", UNSET))

        def _parse_agent_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        agent_name = _parse_agent_name(d.pop("agent_name", UNSET))

        def _parse_check_stage(data: object) -> ControlCheckStage | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ControlCheckStage(data)

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
                return ControlAppliesTo(data)

            except:  # noqa: E722
                pass
            return cast(ControlAppliesTo | None | Unset, data)

        applies_to = _parse_applies_to(d.pop("applies_to", UNSET))

        def _parse_evaluator_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        evaluator_name = _parse_evaluator_name(d.pop("evaluator_name", UNSET))

        def _parse_selector_path(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        selector_path = _parse_selector_path(d.pop("selector_path", UNSET))

        extended_control_span_record = cls(
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
            metric_info=metric_info,
            files=files,
            is_complete=is_complete,
            step_number=step_number,
            control_id=control_id,
            agent_name=agent_name,
            check_stage=check_stage,
            applies_to=applies_to,
            evaluator_name=evaluator_name,
            selector_path=selector_path,
        )

        extended_control_span_record.additional_properties = d
        return extended_control_span_record

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
