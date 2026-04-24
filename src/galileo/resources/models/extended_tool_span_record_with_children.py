import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.content_modality import ContentModality
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
    from ..models.extended_control_span_record import ExtendedControlSpanRecord
    from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
    from ..models.extended_retriever_span_record_with_children import ExtendedRetrieverSpanRecordWithChildren
    from ..models.extended_tool_span_record_with_children_annotation_aggregates import (
        ExtendedToolSpanRecordWithChildrenAnnotationAggregates,
    )
    from ..models.extended_tool_span_record_with_children_annotations import (
        ExtendedToolSpanRecordWithChildrenAnnotations,
    )
    from ..models.extended_tool_span_record_with_children_dataset_metadata import (
        ExtendedToolSpanRecordWithChildrenDatasetMetadata,
    )
    from ..models.extended_tool_span_record_with_children_feedback_rating_info import (
        ExtendedToolSpanRecordWithChildrenFeedbackRatingInfo,
    )
    from ..models.extended_tool_span_record_with_children_files_type_0 import (
        ExtendedToolSpanRecordWithChildrenFilesType0,
    )
    from ..models.extended_tool_span_record_with_children_metric_info_type_0 import (
        ExtendedToolSpanRecordWithChildrenMetricInfoType0,
    )
    from ..models.extended_tool_span_record_with_children_user_metadata import (
        ExtendedToolSpanRecordWithChildrenUserMetadata,
    )
    from ..models.extended_workflow_span_record_with_children import ExtendedWorkflowSpanRecordWithChildren
    from ..models.metrics import Metrics


T = TypeVar("T", bound="ExtendedToolSpanRecordWithChildren")


@_attrs_define
class ExtendedToolSpanRecordWithChildren:
    """
    Attributes
    ----------
        id (str): Galileo ID of the session, trace or span
        session_id (str): Galileo ID of the session containing the trace (or the same value as id for a trace)
        project_id (str): Galileo ID of the project associated with this trace or span
        run_id (str): Galileo ID of the run (log stream or experiment) associated with this trace or span
        parent_id (str): Galileo ID of the parent of this span
        spans (Union[Unset, list[Union['ExtendedAgentSpanRecordWithChildren', 'ExtendedControlSpanRecord',
            'ExtendedLlmSpanRecord', 'ExtendedRetrieverSpanRecordWithChildren', 'ExtendedToolSpanRecordWithChildren',
            'ExtendedWorkflowSpanRecordWithChildren']]]):
        type_ (Union[Literal['tool'], Unset]): Type of the trace, span or session. Default: 'tool'.
        input_ (Union[Unset, str]): Input to the trace or span. Default: ''.
        redacted_input (Union[None, Unset, str]): Redacted input of the trace or span.
        output (Union[None, Unset, str]): Output of the trace or span.
        redacted_output (Union[None, Unset, str]): Redacted output of the trace or span.
        name (Union[Unset, str]): Name of the trace, span or session. Default: ''.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        user_metadata (Union[Unset, ExtendedToolSpanRecordWithChildrenUserMetadata]): Metadata associated with this
            trace or span.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        metrics (Union[Unset, Metrics]):
        external_id (Union[None, Unset, str]): A user-provided session, trace or span ID.
        dataset_input (Union[None, Unset, str]): Input to the dataset associated with this trace
        dataset_output (Union[None, Unset, str]): Output from the dataset associated with this trace
        dataset_metadata (Union[Unset, ExtendedToolSpanRecordWithChildrenDatasetMetadata]): Metadata from the dataset
            associated with this trace
        trace_id (Union[None, Unset, str]): Galileo ID of the trace containing the span (or the same value as id for a
            trace)
        updated_at (Union[None, Unset, datetime.datetime]): Timestamp of the session or trace or span's last update
        has_children (Union[None, Unset, bool]): Whether or not this trace or span has child spans
        metrics_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        session_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        feedback_rating_info (Union[Unset, ExtendedToolSpanRecordWithChildrenFeedbackRatingInfo]): Feedback information
            related to the record
        annotations (Union[Unset, ExtendedToolSpanRecordWithChildrenAnnotations]): Annotations keyed by template ID and
            annotator ID
        file_ids (Union[Unset, list[str]]): IDs of files associated with this record
        file_modalities (Union[Unset, list[ContentModality]]): Modalities of files associated with this record
        annotation_aggregates (Union[Unset, ExtendedToolSpanRecordWithChildrenAnnotationAggregates]): Annotation
            aggregate information keyed by template ID
        annotation_queue_ids (Union[Unset, list[str]]): IDs of annotation queues this record is in
        metric_info (Union['ExtendedToolSpanRecordWithChildrenMetricInfoType0', None, Unset]): Detailed information
            about the metrics associated with this trace or span
        files (Union['ExtendedToolSpanRecordWithChildrenFilesType0', None, Unset]): File metadata keyed by file ID for
            files associated with this record
        is_complete (Union[Unset, bool]): Whether the parent trace is complete or not Default: True.
        step_number (Union[None, Unset, int]): Topological step number of the span.
        tool_call_id (Union[None, Unset, str]): ID of the tool call.
    """

    id: str
    session_id: str
    project_id: str
    run_id: str
    parent_id: str
    spans: (
        Unset
        | list[
            Union[
                "ExtendedAgentSpanRecordWithChildren",
                "ExtendedControlSpanRecord",
                "ExtendedLlmSpanRecord",
                "ExtendedRetrieverSpanRecordWithChildren",
                "ExtendedToolSpanRecordWithChildren",
                "ExtendedWorkflowSpanRecordWithChildren",
            ]
        ]
    ) = UNSET
    type_: Literal["tool"] | Unset = "tool"
    input_: Unset | str = ""
    redacted_input: None | Unset | str = UNSET
    output: None | Unset | str = UNSET
    redacted_output: None | Unset | str = UNSET
    name: Unset | str = ""
    created_at: Unset | datetime.datetime = UNSET
    user_metadata: Union[Unset, "ExtendedToolSpanRecordWithChildrenUserMetadata"] = UNSET
    tags: Unset | list[str] = UNSET
    status_code: None | Unset | int = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    external_id: None | Unset | str = UNSET
    dataset_input: None | Unset | str = UNSET
    dataset_output: None | Unset | str = UNSET
    dataset_metadata: Union[Unset, "ExtendedToolSpanRecordWithChildrenDatasetMetadata"] = UNSET
    trace_id: None | Unset | str = UNSET
    updated_at: None | Unset | datetime.datetime = UNSET
    has_children: None | Unset | bool = UNSET
    metrics_batch_id: None | Unset | str = UNSET
    session_batch_id: None | Unset | str = UNSET
    feedback_rating_info: Union[Unset, "ExtendedToolSpanRecordWithChildrenFeedbackRatingInfo"] = UNSET
    annotations: Union[Unset, "ExtendedToolSpanRecordWithChildrenAnnotations"] = UNSET
    file_ids: Unset | list[str] = UNSET
    file_modalities: Unset | list[ContentModality] = UNSET
    annotation_aggregates: Union[Unset, "ExtendedToolSpanRecordWithChildrenAnnotationAggregates"] = UNSET
    annotation_queue_ids: Unset | list[str] = UNSET
    metric_info: Union["ExtendedToolSpanRecordWithChildrenMetricInfoType0", None, Unset] = UNSET
    files: Union["ExtendedToolSpanRecordWithChildrenFilesType0", None, Unset] = UNSET
    is_complete: Unset | bool = True
    step_number: None | Unset | int = UNSET
    tool_call_id: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
        from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
        from ..models.extended_retriever_span_record_with_children import ExtendedRetrieverSpanRecordWithChildren
        from ..models.extended_tool_span_record_with_children_files_type_0 import (
            ExtendedToolSpanRecordWithChildrenFilesType0,
        )
        from ..models.extended_tool_span_record_with_children_metric_info_type_0 import (
            ExtendedToolSpanRecordWithChildrenMetricInfoType0,
        )
        from ..models.extended_workflow_span_record_with_children import ExtendedWorkflowSpanRecordWithChildren

        id = self.id

        session_id = self.session_id

        project_id = self.project_id

        run_id = self.run_id

        parent_id = self.parent_id

        spans: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.spans, Unset):
            spans = []
            for spans_item_data in self.spans:
                spans_item: dict[str, Any]
                if isinstance(
                    spans_item_data,
                    ExtendedAgentSpanRecordWithChildren
                    | ExtendedWorkflowSpanRecordWithChildren
                    | ExtendedLlmSpanRecord
                    | ExtendedToolSpanRecordWithChildren
                    | ExtendedRetrieverSpanRecordWithChildren,
                ):
                    spans_item = spans_item_data.to_dict()
                else:
                    spans_item = spans_item_data.to_dict()

                spans.append(spans_item)

        type_ = self.type_

        input_ = self.input_

        redacted_input: None | Unset | str
        redacted_input = UNSET if isinstance(self.redacted_input, Unset) else self.redacted_input

        output: None | Unset | str
        output = UNSET if isinstance(self.output, Unset) else self.output

        redacted_output: None | Unset | str
        redacted_output = UNSET if isinstance(self.redacted_output, Unset) else self.redacted_output

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
        elif isinstance(self.metric_info, ExtendedToolSpanRecordWithChildrenMetricInfoType0):
            metric_info = self.metric_info.to_dict()
        else:
            metric_info = self.metric_info

        files: None | Unset | dict[str, Any]
        if isinstance(self.files, Unset):
            files = UNSET
        elif isinstance(self.files, ExtendedToolSpanRecordWithChildrenFilesType0):
            files = self.files.to_dict()
        else:
            files = self.files

        is_complete = self.is_complete

        step_number: None | Unset | int
        step_number = UNSET if isinstance(self.step_number, Unset) else self.step_number

        tool_call_id: None | Unset | str
        tool_call_id = UNSET if isinstance(self.tool_call_id, Unset) else self.tool_call_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "session_id": session_id, "project_id": project_id, "run_id": run_id, "parent_id": parent_id}
        )
        if spans is not UNSET:
            field_dict["spans"] = spans
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
        if tool_call_id is not UNSET:
            field_dict["tool_call_id"] = tool_call_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
        from ..models.extended_control_span_record import ExtendedControlSpanRecord
        from ..models.extended_retriever_span_record_with_children import ExtendedRetrieverSpanRecordWithChildren
        from ..models.extended_tool_span_record_with_children_annotation_aggregates import (
            ExtendedToolSpanRecordWithChildrenAnnotationAggregates,
        )
        from ..models.extended_tool_span_record_with_children_annotations import (
            ExtendedToolSpanRecordWithChildrenAnnotations,
        )
        from ..models.extended_tool_span_record_with_children_dataset_metadata import (
            ExtendedToolSpanRecordWithChildrenDatasetMetadata,
        )
        from ..models.extended_tool_span_record_with_children_feedback_rating_info import (
            ExtendedToolSpanRecordWithChildrenFeedbackRatingInfo,
        )
        from ..models.extended_tool_span_record_with_children_files_type_0 import (
            ExtendedToolSpanRecordWithChildrenFilesType0,
        )
        from ..models.extended_tool_span_record_with_children_metric_info_type_0 import (
            ExtendedToolSpanRecordWithChildrenMetricInfoType0,
        )
        from ..models.extended_tool_span_record_with_children_user_metadata import (
            ExtendedToolSpanRecordWithChildrenUserMetadata,
        )
        from ..models.extended_workflow_span_record_with_children import ExtendedWorkflowSpanRecordWithChildren
        from ..models.metrics import Metrics

        d = dict(src_dict)
        id = d.pop("id")

        session_id = d.pop("session_id")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        parent_id = d.pop("parent_id")

        spans = []
        _spans = d.pop("spans", UNSET)
        for spans_item_data in _spans or []:

            def _parse_spans_item(
                data: object,
            ) -> Union[
                "ExtendedAgentSpanRecordWithChildren",
                "ExtendedControlSpanRecord",
                "ExtendedLlmSpanRecord",
                "ExtendedRetrieverSpanRecordWithChildren",
                "ExtendedToolSpanRecordWithChildren",
                "ExtendedWorkflowSpanRecordWithChildren",
            ]:
                # Discriminator-aware parsing for Extended*Record types
                if isinstance(data, dict) and "type" in data:
                    type_value = data.get("type")

                    # Hardcoded discriminator mapping for Extended*Record types
                    if type_value == "trace":
                        try:
                            from ..models.extended_trace_record import ExtendedTraceRecord

                            return ExtendedTraceRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "agent":
                        try:
                            from ..models.extended_agent_span_record import ExtendedAgentSpanRecord

                            return ExtendedAgentSpanRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "workflow":
                        try:
                            from ..models.extended_workflow_span_record import ExtendedWorkflowSpanRecord

                            return ExtendedWorkflowSpanRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "llm":
                        try:
                            from ..models.extended_llm_span_record import ExtendedLlmSpanRecord

                            return ExtendedLlmSpanRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "tool":
                        try:
                            from ..models.extended_tool_span_record import ExtendedToolSpanRecord

                            return ExtendedToolSpanRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "retriever":
                        try:
                            from ..models.extended_retriever_span_record import ExtendedRetrieverSpanRecord

                            return ExtendedRetrieverSpanRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "session":
                        try:
                            from ..models.extended_session_record import ExtendedSessionRecord

                            return ExtendedSessionRecord.from_dict(data)
                        except:  # noqa: E722
                            pass

                # Fallback to standard union parsing
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedAgentSpanRecordWithChildren.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedWorkflowSpanRecordWithChildren.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedLlmSpanRecord.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedToolSpanRecordWithChildren.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedRetrieverSpanRecordWithChildren.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedControlSpanRecord.from_dict(data)

                except:  # noqa: E722
                    pass
                # If we reach here, none of the parsers succeeded
                discriminator_info = f" (type={data.get('type')})" if isinstance(data, dict) and "type" in data else ""
                raise ValueError(f"Could not parse union type for spans_item{discriminator_info}")

            spans_item = _parse_spans_item(spans_item_data)

            spans.append(spans_item)

        type_ = cast(Literal["tool"] | Unset, d.pop("type", UNSET))
        if type_ != "tool" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'tool', got '{type_}'")

        input_ = d.pop("input", UNSET)

        def _parse_redacted_input(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        def _parse_output(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        output = _parse_output(d.pop("output", UNSET))

        def _parse_redacted_output(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Unset | datetime.datetime
        created_at = UNSET if isinstance(_created_at, Unset) else isoparse(_created_at)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Unset | ExtendedToolSpanRecordWithChildrenUserMetadata
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = ExtendedToolSpanRecordWithChildrenUserMetadata.from_dict(_user_metadata)

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
        dataset_metadata: Unset | ExtendedToolSpanRecordWithChildrenDatasetMetadata
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = ExtendedToolSpanRecordWithChildrenDatasetMetadata.from_dict(_dataset_metadata)

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
        feedback_rating_info: Unset | ExtendedToolSpanRecordWithChildrenFeedbackRatingInfo
        if isinstance(_feedback_rating_info, Unset):
            feedback_rating_info = UNSET
        else:
            feedback_rating_info = ExtendedToolSpanRecordWithChildrenFeedbackRatingInfo.from_dict(_feedback_rating_info)

        _annotations = d.pop("annotations", UNSET)
        annotations: Unset | ExtendedToolSpanRecordWithChildrenAnnotations
        if isinstance(_annotations, Unset):
            annotations = UNSET
        else:
            annotations = ExtendedToolSpanRecordWithChildrenAnnotations.from_dict(_annotations)

        file_ids = cast(list[str], d.pop("file_ids", UNSET))

        file_modalities = []
        _file_modalities = d.pop("file_modalities", UNSET)
        for file_modalities_item_data in _file_modalities or []:
            file_modalities_item = ContentModality(file_modalities_item_data)

            file_modalities.append(file_modalities_item)

        _annotation_aggregates = d.pop("annotation_aggregates", UNSET)
        annotation_aggregates: Unset | ExtendedToolSpanRecordWithChildrenAnnotationAggregates
        if isinstance(_annotation_aggregates, Unset):
            annotation_aggregates = UNSET
        else:
            annotation_aggregates = ExtendedToolSpanRecordWithChildrenAnnotationAggregates.from_dict(
                _annotation_aggregates
            )

        annotation_queue_ids = cast(list[str], d.pop("annotation_queue_ids", UNSET))

        def _parse_metric_info(data: object) -> Union["ExtendedToolSpanRecordWithChildrenMetricInfoType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExtendedToolSpanRecordWithChildrenMetricInfoType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ExtendedToolSpanRecordWithChildrenMetricInfoType0", None, Unset], data)

        metric_info = _parse_metric_info(d.pop("metric_info", UNSET))

        def _parse_files(data: object) -> Union["ExtendedToolSpanRecordWithChildrenFilesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExtendedToolSpanRecordWithChildrenFilesType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ExtendedToolSpanRecordWithChildrenFilesType0", None, Unset], data)

        files = _parse_files(d.pop("files", UNSET))

        is_complete = d.pop("is_complete", UNSET)

        def _parse_step_number(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        step_number = _parse_step_number(d.pop("step_number", UNSET))

        def _parse_tool_call_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        tool_call_id = _parse_tool_call_id(d.pop("tool_call_id", UNSET))

        extended_tool_span_record_with_children = cls(
            id=id,
            session_id=session_id,
            project_id=project_id,
            run_id=run_id,
            parent_id=parent_id,
            spans=spans,
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
            tool_call_id=tool_call_id,
        )

        extended_tool_span_record_with_children.additional_properties = d
        return extended_tool_span_record_with_children

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
