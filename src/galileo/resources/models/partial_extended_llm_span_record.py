from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.content_modality import ContentModality
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.image_generation_event import ImageGenerationEvent
    from ..models.internal_tool_call import InternalToolCall
    from ..models.llm_metrics import LlmMetrics
    from ..models.mcp_approval_request_event import MCPApprovalRequestEvent
    from ..models.mcp_call_event import MCPCallEvent
    from ..models.mcp_list_tools_event import MCPListToolsEvent
    from ..models.message import Message
    from ..models.message_event import MessageEvent
    from ..models.partial_extended_llm_span_record_annotation_aggregates import (
        PartialExtendedLlmSpanRecordAnnotationAggregates,
    )
    from ..models.partial_extended_llm_span_record_annotations import PartialExtendedLlmSpanRecordAnnotations
    from ..models.partial_extended_llm_span_record_dataset_metadata import PartialExtendedLlmSpanRecordDatasetMetadata
    from ..models.partial_extended_llm_span_record_feedback_rating_info import (
        PartialExtendedLlmSpanRecordFeedbackRatingInfo,
    )
    from ..models.partial_extended_llm_span_record_files_type_0 import PartialExtendedLlmSpanRecordFilesType0
    from ..models.partial_extended_llm_span_record_metric_info_type_0 import PartialExtendedLlmSpanRecordMetricInfoType0
    from ..models.partial_extended_llm_span_record_tools_type_0_item import PartialExtendedLlmSpanRecordToolsType0Item
    from ..models.partial_extended_llm_span_record_user_metadata import PartialExtendedLlmSpanRecordUserMetadata
    from ..models.reasoning_event import ReasoningEvent
    from ..models.web_search_call_event import WebSearchCallEvent


T = TypeVar("T", bound="PartialExtendedLlmSpanRecord")


@_attrs_define
class PartialExtendedLlmSpanRecord:
    """
    Attributes:
        type_ (Literal['llm'] | Unset): Type of the trace, span or session. Default: 'llm'.
        input_ (list[Message] | Unset): Input to the trace or span.
        redacted_input (list[Message] | None | Unset): Redacted input of the trace or span.
        output (Message | Unset):
        redacted_output (Message | None | Unset): Redacted output of the trace or span.
        name (str | Unset): Name of the trace, span or session. Default: ''.
        created_at (datetime.datetime | Unset): Timestamp of the trace or span's creation.
        user_metadata (PartialExtendedLlmSpanRecordUserMetadata | Unset): Metadata associated with this trace or span.
        tags (list[str] | Unset): Tags associated with this trace or span.
        status_code (int | None | Unset): Status code of the trace or span. Used for logging failure or error states.
        metrics (LlmMetrics | Unset):
        external_id (None | str | Unset): A user-provided session, trace or span ID.
        dataset_input (None | str | Unset): Input to the dataset associated with this trace
        dataset_output (None | str | Unset): Output from the dataset associated with this trace
        dataset_metadata (PartialExtendedLlmSpanRecordDatasetMetadata | Unset): Metadata from the dataset associated
            with this trace
        id (None | Unset | UUID): Galileo ID of the session, trace or span
        session_id (None | Unset | UUID): Galileo ID of the session containing the trace (or the same value as id for a
            trace)
        trace_id (None | str | Unset): Galileo ID of the trace containing the span (or the same value as id for a trace)
        project_id (None | Unset | UUID): Galileo ID of the project associated with this trace or span
        run_id (None | Unset | UUID): Galileo ID of the run (log stream or experiment) associated with this trace or
            span
        updated_at (datetime.datetime | None | Unset): Timestamp of the session or trace or span's last update
        has_children (bool | None | Unset): Whether or not this trace or span has child spans
        metrics_batch_id (None | str | Unset): Galileo ID of the metrics batch associated with this trace or span
        session_batch_id (None | str | Unset): Galileo ID of the metrics batch associated with this trace or span
        feedback_rating_info (PartialExtendedLlmSpanRecordFeedbackRatingInfo | Unset): Feedback information related to
            the record
        annotations (PartialExtendedLlmSpanRecordAnnotations | Unset): Annotations keyed by template ID and annotator ID
        file_ids (list[str] | Unset): IDs of files associated with this record
        file_modalities (list[ContentModality] | Unset): Modalities of files associated with this record
        annotation_aggregates (PartialExtendedLlmSpanRecordAnnotationAggregates | Unset): Annotation aggregate
            information keyed by template ID
        annotation_queue_ids (list[str] | Unset): IDs of annotation queues this record is in
        metric_info (None | PartialExtendedLlmSpanRecordMetricInfoType0 | Unset): Detailed information about the metrics
            associated with this trace or span
        files (None | PartialExtendedLlmSpanRecordFilesType0 | Unset): File metadata keyed by file ID for files
            associated with this record
        parent_id (None | Unset | UUID): Galileo ID of the parent of this span
        is_complete (bool | Unset): Whether the parent trace is complete or not Default: True.
        step_number (int | None | Unset): Topological step number of the span.
        tools (list[PartialExtendedLlmSpanRecordToolsType0Item] | None | Unset): List of available tools passed to the
            LLM on invocation.
        events (list[ImageGenerationEvent | InternalToolCall | MCPApprovalRequestEvent | MCPCallEvent |
            MCPListToolsEvent | MessageEvent | ReasoningEvent | WebSearchCallEvent] | None | Unset): List of reasoning,
            internal tool call, or MCP events that occurred during the LLM span.
        model (None | str | Unset): Model used for this span.
        temperature (float | None | Unset): Temperature used for generation.
        finish_reason (None | str | Unset): Reason for finishing.
    """

    type_: Literal["llm"] | Unset = "llm"
    input_: list[Message] | Unset = UNSET
    redacted_input: list[Message] | None | Unset = UNSET
    output: Message | Unset = UNSET
    redacted_output: Message | None | Unset = UNSET
    name: str | Unset = ""
    created_at: datetime.datetime | Unset = UNSET
    user_metadata: PartialExtendedLlmSpanRecordUserMetadata | Unset = UNSET
    tags: list[str] | Unset = UNSET
    status_code: int | None | Unset = UNSET
    metrics: LlmMetrics | Unset = UNSET
    external_id: None | str | Unset = UNSET
    dataset_input: None | str | Unset = UNSET
    dataset_output: None | str | Unset = UNSET
    dataset_metadata: PartialExtendedLlmSpanRecordDatasetMetadata | Unset = UNSET
    id: None | Unset | UUID = UNSET
    session_id: None | Unset | UUID = UNSET
    trace_id: None | str | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    run_id: None | Unset | UUID = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    has_children: bool | None | Unset = UNSET
    metrics_batch_id: None | str | Unset = UNSET
    session_batch_id: None | str | Unset = UNSET
    feedback_rating_info: PartialExtendedLlmSpanRecordFeedbackRatingInfo | Unset = UNSET
    annotations: PartialExtendedLlmSpanRecordAnnotations | Unset = UNSET
    file_ids: list[str] | Unset = UNSET
    file_modalities: list[ContentModality] | Unset = UNSET
    annotation_aggregates: PartialExtendedLlmSpanRecordAnnotationAggregates | Unset = UNSET
    annotation_queue_ids: list[str] | Unset = UNSET
    metric_info: None | PartialExtendedLlmSpanRecordMetricInfoType0 | Unset = UNSET
    files: None | PartialExtendedLlmSpanRecordFilesType0 | Unset = UNSET
    parent_id: None | Unset | UUID = UNSET
    is_complete: bool | Unset = True
    step_number: int | None | Unset = UNSET
    tools: list[PartialExtendedLlmSpanRecordToolsType0Item] | None | Unset = UNSET
    events: (
        list[
            ImageGenerationEvent
            | InternalToolCall
            | MCPApprovalRequestEvent
            | MCPCallEvent
            | MCPListToolsEvent
            | MessageEvent
            | ReasoningEvent
            | WebSearchCallEvent
        ]
        | None
        | Unset
    ) = UNSET
    model: None | str | Unset = UNSET
    temperature: float | None | Unset = UNSET
    finish_reason: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.image_generation_event import ImageGenerationEvent
        from ..models.internal_tool_call import InternalToolCall
        from ..models.mcp_call_event import MCPCallEvent
        from ..models.mcp_list_tools_event import MCPListToolsEvent
        from ..models.message import Message
        from ..models.message_event import MessageEvent
        from ..models.partial_extended_llm_span_record_files_type_0 import PartialExtendedLlmSpanRecordFilesType0
        from ..models.partial_extended_llm_span_record_metric_info_type_0 import (
            PartialExtendedLlmSpanRecordMetricInfoType0,
        )
        from ..models.reasoning_event import ReasoningEvent
        from ..models.web_search_call_event import WebSearchCallEvent

        type_ = self.type_

        input_: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.input_, Unset):
            input_ = []
            for input_item_data in self.input_:
                input_item = input_item_data.to_dict()
                input_.append(input_item)

        redacted_input: list[dict[str, Any]] | None | Unset
        if isinstance(self.redacted_input, Unset):
            redacted_input = UNSET
        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_0_item_data in self.redacted_input:
                redacted_input_type_0_item = redacted_input_type_0_item_data.to_dict()
                redacted_input.append(redacted_input_type_0_item)

        else:
            redacted_input = self.redacted_input

        output: dict[str, Any] | Unset = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        redacted_output: dict[str, Any] | None | Unset
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        elif isinstance(self.redacted_output, Message):
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

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        session_id: None | str | Unset
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        elif isinstance(self.session_id, UUID):
            session_id = str(self.session_id)
        else:
            session_id = self.session_id

        trace_id: None | str | Unset
        if isinstance(self.trace_id, Unset):
            trace_id = UNSET
        else:
            trace_id = self.trace_id

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        run_id: None | str | Unset
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        elif isinstance(self.run_id, UUID):
            run_id = str(self.run_id)
        else:
            run_id = self.run_id

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

        metric_info: dict[str, Any] | None | Unset
        if isinstance(self.metric_info, Unset):
            metric_info = UNSET
        elif isinstance(self.metric_info, PartialExtendedLlmSpanRecordMetricInfoType0):
            metric_info = self.metric_info.to_dict()
        else:
            metric_info = self.metric_info

        files: dict[str, Any] | None | Unset
        if isinstance(self.files, Unset):
            files = UNSET
        elif isinstance(self.files, PartialExtendedLlmSpanRecordFilesType0):
            files = self.files.to_dict()
        else:
            files = self.files

        parent_id: None | str | Unset
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        elif isinstance(self.parent_id, UUID):
            parent_id = str(self.parent_id)
        else:
            parent_id = self.parent_id

        is_complete = self.is_complete

        step_number: int | None | Unset
        if isinstance(self.step_number, Unset):
            step_number = UNSET
        else:
            step_number = self.step_number

        tools: list[dict[str, Any]] | None | Unset
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)

        else:
            tools = self.tools

        events: list[dict[str, Any]] | None | Unset
        if isinstance(self.events, Unset):
            events = UNSET
        elif isinstance(self.events, list):
            events = []
            for events_type_0_item_data in self.events:
                events_type_0_item: dict[str, Any]
                if isinstance(events_type_0_item_data, MessageEvent):
                    events_type_0_item = events_type_0_item_data.to_dict()
                elif isinstance(events_type_0_item_data, ReasoningEvent):
                    events_type_0_item = events_type_0_item_data.to_dict()
                elif isinstance(events_type_0_item_data, InternalToolCall):
                    events_type_0_item = events_type_0_item_data.to_dict()
                elif isinstance(events_type_0_item_data, WebSearchCallEvent):
                    events_type_0_item = events_type_0_item_data.to_dict()
                elif isinstance(events_type_0_item_data, ImageGenerationEvent):
                    events_type_0_item = events_type_0_item_data.to_dict()
                elif isinstance(events_type_0_item_data, MCPCallEvent):
                    events_type_0_item = events_type_0_item_data.to_dict()
                elif isinstance(events_type_0_item_data, MCPListToolsEvent):
                    events_type_0_item = events_type_0_item_data.to_dict()
                else:
                    events_type_0_item = events_type_0_item_data.to_dict()

                events.append(events_type_0_item)

        else:
            events = self.events

        model: None | str | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        temperature: float | None | Unset
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        finish_reason: None | str | Unset
        if isinstance(self.finish_reason, Unset):
            finish_reason = UNSET
        else:
            finish_reason = self.finish_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        if id is not UNSET:
            field_dict["id"] = id
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if trace_id is not UNSET:
            field_dict["trace_id"] = trace_id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if run_id is not UNSET:
            field_dict["run_id"] = run_id
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
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if is_complete is not UNSET:
            field_dict["is_complete"] = is_complete
        if step_number is not UNSET:
            field_dict["step_number"] = step_number
        if tools is not UNSET:
            field_dict["tools"] = tools
        if events is not UNSET:
            field_dict["events"] = events
        if model is not UNSET:
            field_dict["model"] = model
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if finish_reason is not UNSET:
            field_dict["finish_reason"] = finish_reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.image_generation_event import ImageGenerationEvent
        from ..models.internal_tool_call import InternalToolCall
        from ..models.llm_metrics import LlmMetrics
        from ..models.mcp_approval_request_event import MCPApprovalRequestEvent
        from ..models.mcp_call_event import MCPCallEvent
        from ..models.mcp_list_tools_event import MCPListToolsEvent
        from ..models.message import Message
        from ..models.message_event import MessageEvent
        from ..models.partial_extended_llm_span_record_annotation_aggregates import (
            PartialExtendedLlmSpanRecordAnnotationAggregates,
        )
        from ..models.partial_extended_llm_span_record_annotations import PartialExtendedLlmSpanRecordAnnotations
        from ..models.partial_extended_llm_span_record_dataset_metadata import (
            PartialExtendedLlmSpanRecordDatasetMetadata,
        )
        from ..models.partial_extended_llm_span_record_feedback_rating_info import (
            PartialExtendedLlmSpanRecordFeedbackRatingInfo,
        )
        from ..models.partial_extended_llm_span_record_files_type_0 import PartialExtendedLlmSpanRecordFilesType0
        from ..models.partial_extended_llm_span_record_metric_info_type_0 import (
            PartialExtendedLlmSpanRecordMetricInfoType0,
        )
        from ..models.partial_extended_llm_span_record_tools_type_0_item import (
            PartialExtendedLlmSpanRecordToolsType0Item,
        )
        from ..models.partial_extended_llm_span_record_user_metadata import PartialExtendedLlmSpanRecordUserMetadata
        from ..models.reasoning_event import ReasoningEvent
        from ..models.web_search_call_event import WebSearchCallEvent

        d = dict(src_dict)
        type_ = cast(Literal["llm"] | Unset, d.pop("type", UNSET))
        if type_ != "llm" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'llm', got '{type_}'")

        _input_ = d.pop("input", UNSET)
        input_: list[Message] | Unset = UNSET
        if _input_ is not UNSET:
            input_ = []
            for input_item_data in _input_:
                input_item = Message.from_dict(input_item_data)

                input_.append(input_item)

        def _parse_redacted_input(data: object) -> list[Message] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_0 = []
                _redacted_input_type_0 = data
                for redacted_input_type_0_item_data in _redacted_input_type_0:
                    redacted_input_type_0_item = Message.from_dict(redacted_input_type_0_item_data)

                    redacted_input_type_0.append(redacted_input_type_0_item)

                return redacted_input_type_0
            except:  # noqa: E722
                pass
            return cast(list[Message] | None | Unset, data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        _output = d.pop("output", UNSET)
        output: Message | Unset
        if isinstance(_output, Unset):
            output = UNSET
        else:
            output = Message.from_dict(_output)

        def _parse_redacted_output(data: object) -> Message | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_output_type_0 = Message.from_dict(data)

                return redacted_output_type_0
            except:  # noqa: E722
                pass
            return cast(Message | None | Unset, data)

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: PartialExtendedLlmSpanRecordUserMetadata | Unset
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = PartialExtendedLlmSpanRecordUserMetadata.from_dict(_user_metadata)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_status_code(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: LlmMetrics | Unset
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = LlmMetrics.from_dict(_metrics)

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
        dataset_metadata: PartialExtendedLlmSpanRecordDatasetMetadata | Unset
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = PartialExtendedLlmSpanRecordDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)

                return id_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | UUID, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_session_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                session_id_type_0 = UUID(data)

                return session_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | UUID, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_trace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trace_id = _parse_trace_id(d.pop("trace_id", UNSET))

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_id_type_0 = UUID(data)

                return run_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | UUID, data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

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
        feedback_rating_info: PartialExtendedLlmSpanRecordFeedbackRatingInfo | Unset
        if isinstance(_feedback_rating_info, Unset):
            feedback_rating_info = UNSET
        else:
            feedback_rating_info = PartialExtendedLlmSpanRecordFeedbackRatingInfo.from_dict(_feedback_rating_info)

        _annotations = d.pop("annotations", UNSET)
        annotations: PartialExtendedLlmSpanRecordAnnotations | Unset
        if isinstance(_annotations, Unset):
            annotations = UNSET
        else:
            annotations = PartialExtendedLlmSpanRecordAnnotations.from_dict(_annotations)

        file_ids = cast(list[str], d.pop("file_ids", UNSET))

        _file_modalities = d.pop("file_modalities", UNSET)
        file_modalities: list[ContentModality] | Unset = UNSET
        if _file_modalities is not UNSET:
            file_modalities = []
            for file_modalities_item_data in _file_modalities:
                file_modalities_item = ContentModality(file_modalities_item_data)

                file_modalities.append(file_modalities_item)

        _annotation_aggregates = d.pop("annotation_aggregates", UNSET)
        annotation_aggregates: PartialExtendedLlmSpanRecordAnnotationAggregates | Unset
        if isinstance(_annotation_aggregates, Unset):
            annotation_aggregates = UNSET
        else:
            annotation_aggregates = PartialExtendedLlmSpanRecordAnnotationAggregates.from_dict(_annotation_aggregates)

        annotation_queue_ids = cast(list[str], d.pop("annotation_queue_ids", UNSET))

        def _parse_metric_info(data: object) -> None | PartialExtendedLlmSpanRecordMetricInfoType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_info_type_0 = PartialExtendedLlmSpanRecordMetricInfoType0.from_dict(data)

                return metric_info_type_0
            except:  # noqa: E722
                pass
            return cast(None | PartialExtendedLlmSpanRecordMetricInfoType0 | Unset, data)

        metric_info = _parse_metric_info(d.pop("metric_info", UNSET))

        def _parse_files(data: object) -> None | PartialExtendedLlmSpanRecordFilesType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                files_type_0 = PartialExtendedLlmSpanRecordFilesType0.from_dict(data)

                return files_type_0
            except:  # noqa: E722
                pass
            return cast(None | PartialExtendedLlmSpanRecordFilesType0 | Unset, data)

        files = _parse_files(d.pop("files", UNSET))

        def _parse_parent_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                parent_id_type_0 = UUID(data)

                return parent_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | UUID, data)

        parent_id = _parse_parent_id(d.pop("parent_id", UNSET))

        is_complete = d.pop("is_complete", UNSET)

        def _parse_step_number(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        step_number = _parse_step_number(d.pop("step_number", UNSET))

        def _parse_tools(data: object) -> list[PartialExtendedLlmSpanRecordToolsType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0 = []
                _tools_type_0 = data
                for tools_type_0_item_data in _tools_type_0:
                    tools_type_0_item = PartialExtendedLlmSpanRecordToolsType0Item.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except:  # noqa: E722
                pass
            return cast(list[PartialExtendedLlmSpanRecordToolsType0Item] | None | Unset, data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_events(
            data: object,
        ) -> (
            list[
                ImageGenerationEvent
                | InternalToolCall
                | MCPApprovalRequestEvent
                | MCPCallEvent
                | MCPListToolsEvent
                | MessageEvent
                | ReasoningEvent
                | WebSearchCallEvent
            ]
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                events_type_0 = []
                _events_type_0 = data
                for events_type_0_item_data in _events_type_0:

                    def _parse_events_type_0_item(
                        data: object,
                    ) -> (
                        ImageGenerationEvent
                        | InternalToolCall
                        | MCPApprovalRequestEvent
                        | MCPCallEvent
                        | MCPListToolsEvent
                        | MessageEvent
                        | ReasoningEvent
                        | WebSearchCallEvent
                    ):
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            events_type_0_item_type_0 = MessageEvent.from_dict(data)

                            return events_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            events_type_0_item_type_1 = ReasoningEvent.from_dict(data)

                            return events_type_0_item_type_1
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            events_type_0_item_type_2 = InternalToolCall.from_dict(data)

                            return events_type_0_item_type_2
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            events_type_0_item_type_3 = WebSearchCallEvent.from_dict(data)

                            return events_type_0_item_type_3
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            events_type_0_item_type_4 = ImageGenerationEvent.from_dict(data)

                            return events_type_0_item_type_4
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            events_type_0_item_type_5 = MCPCallEvent.from_dict(data)

                            return events_type_0_item_type_5
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            events_type_0_item_type_6 = MCPListToolsEvent.from_dict(data)

                            return events_type_0_item_type_6
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        events_type_0_item_type_7 = MCPApprovalRequestEvent.from_dict(data)

                        return events_type_0_item_type_7

                    events_type_0_item = _parse_events_type_0_item(events_type_0_item_data)

                    events_type_0.append(events_type_0_item)

                return events_type_0
            except:  # noqa: E722
                pass
            return cast(
                list[
                    ImageGenerationEvent
                    | InternalToolCall
                    | MCPApprovalRequestEvent
                    | MCPCallEvent
                    | MCPListToolsEvent
                    | MessageEvent
                    | ReasoningEvent
                    | WebSearchCallEvent
                ]
                | None
                | Unset,
                data,
            )

        events = _parse_events(d.pop("events", UNSET))

        def _parse_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_temperature(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_finish_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        finish_reason = _parse_finish_reason(d.pop("finish_reason", UNSET))

        partial_extended_llm_span_record = cls(
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
            id=id,
            session_id=session_id,
            trace_id=trace_id,
            project_id=project_id,
            run_id=run_id,
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
            parent_id=parent_id,
            is_complete=is_complete,
            step_number=step_number,
            tools=tools,
            events=events,
            model=model,
            temperature=temperature,
            finish_reason=finish_reason,
        )

        partial_extended_llm_span_record.additional_properties = d
        return partial_extended_llm_span_record

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
