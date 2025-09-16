import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
    from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
    from ..models.extended_retriever_span_record_with_children import ExtendedRetrieverSpanRecordWithChildren
    from ..models.extended_tool_span_record_with_children import ExtendedToolSpanRecordWithChildren
    from ..models.extended_trace_record_with_children_dataset_metadata import (
        ExtendedTraceRecordWithChildrenDatasetMetadata,
    )
    from ..models.extended_trace_record_with_children_feedback_rating_info import (
        ExtendedTraceRecordWithChildrenFeedbackRatingInfo,
    )
    from ..models.extended_trace_record_with_children_metric_info_type_0 import (
        ExtendedTraceRecordWithChildrenMetricInfoType0,
    )
    from ..models.extended_trace_record_with_children_user_metadata import ExtendedTraceRecordWithChildrenUserMetadata
    from ..models.extended_workflow_span_record_with_children import ExtendedWorkflowSpanRecordWithChildren
    from ..models.metrics import Metrics


T = TypeVar("T", bound="ExtendedTraceRecordWithChildren")


@_attrs_define
class ExtendedTraceRecordWithChildren:
    """
    Attributes:
        id (str): Galileo ID of the trace
        project_id (str): Galileo ID of the project associated with this trace or span
        run_id (str): Galileo ID of the run (log stream or experiment) associated with this trace or span
        session_id (str): Galileo ID of the session containing the trace (or the same value as id for a trace)
        trace_id (str): Galileo ID of the trace containing the span (or the same value as id for a trace)
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        dataset_input (Union[None, Unset, str]): Input to the dataset associated with this trace
        dataset_metadata (Union[Unset, ExtendedTraceRecordWithChildrenDatasetMetadata]): Metadata from the dataset
            associated with this trace
        dataset_output (Union[None, Unset, str]): Output from the dataset associated with this trace
        external_id (Union[None, Unset, str]): A user-provided session, trace or span ID.
        feedback_rating_info (Union[Unset, ExtendedTraceRecordWithChildrenFeedbackRatingInfo]): Feedback information
            related to the trace
        has_children (Union[None, Unset, bool]): Whether or not this trace or span has child spans
        input_ (Union[Unset, str]): Input to the trace or span. Default: ''.
        is_complete (Union[Unset, bool]): Whether the trace is complete or not Default: True.
        metric_info (Union['ExtendedTraceRecordWithChildrenMetricInfoType0', None, Unset]): Detailed information about
            the metrics associated with this trace or span
        metrics (Union[Unset, Metrics]):
        metrics_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        name (Union[Unset, str]): Name of the trace, span or session. Default: ''.
        output (Union[None, Unset, str]): Output of the trace or span.
        redacted_input (Union[None, Unset, str]): Redacted input of the trace or span.
        redacted_output (Union[None, Unset, str]): Redacted output of the trace or span.
        session_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        spans (Union[Unset, list[Union['ExtendedAgentSpanRecordWithChildren', 'ExtendedLlmSpanRecord',
            'ExtendedRetrieverSpanRecordWithChildren', 'ExtendedToolSpanRecordWithChildren',
            'ExtendedWorkflowSpanRecordWithChildren']]]):
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        type_ (Union[Literal['trace'], Unset]): Type of the trace, span or session. Default: 'trace'.
        updated_at (Union[None, Unset, datetime.datetime]): Timestamp of the session or trace or span's last update
        user_metadata (Union[Unset, ExtendedTraceRecordWithChildrenUserMetadata]): Metadata associated with this trace
            or span.
    """

    id: str
    project_id: str
    run_id: str
    session_id: str
    trace_id: str
    created_at: Union[Unset, datetime.datetime] = UNSET
    dataset_input: Union[None, Unset, str] = UNSET
    dataset_metadata: Union[Unset, "ExtendedTraceRecordWithChildrenDatasetMetadata"] = UNSET
    dataset_output: Union[None, Unset, str] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    feedback_rating_info: Union[Unset, "ExtendedTraceRecordWithChildrenFeedbackRatingInfo"] = UNSET
    has_children: Union[None, Unset, bool] = UNSET
    input_: Union[Unset, str] = ""
    is_complete: Union[Unset, bool] = True
    metric_info: Union["ExtendedTraceRecordWithChildrenMetricInfoType0", None, Unset] = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    metrics_batch_id: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = ""
    output: Union[None, Unset, str] = UNSET
    redacted_input: Union[None, Unset, str] = UNSET
    redacted_output: Union[None, Unset, str] = UNSET
    session_batch_id: Union[None, Unset, str] = UNSET
    spans: Union[
        Unset,
        list[
            Union[
                "ExtendedAgentSpanRecordWithChildren",
                "ExtendedLlmSpanRecord",
                "ExtendedRetrieverSpanRecordWithChildren",
                "ExtendedToolSpanRecordWithChildren",
                "ExtendedWorkflowSpanRecordWithChildren",
            ]
        ],
    ] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    type_: Union[Literal["trace"], Unset] = "trace"
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    user_metadata: Union[Unset, "ExtendedTraceRecordWithChildrenUserMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
        from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
        from ..models.extended_tool_span_record_with_children import ExtendedToolSpanRecordWithChildren
        from ..models.extended_trace_record_with_children_metric_info_type_0 import (
            ExtendedTraceRecordWithChildrenMetricInfoType0,
        )
        from ..models.extended_workflow_span_record_with_children import ExtendedWorkflowSpanRecordWithChildren

        id = self.id

        project_id = self.project_id

        run_id = self.run_id

        session_id = self.session_id

        trace_id = self.trace_id

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        dataset_input: Union[None, Unset, str]
        if isinstance(self.dataset_input, Unset):
            dataset_input = UNSET
        else:
            dataset_input = self.dataset_input

        dataset_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.dataset_metadata, Unset):
            dataset_metadata = self.dataset_metadata.to_dict()

        dataset_output: Union[None, Unset, str]
        if isinstance(self.dataset_output, Unset):
            dataset_output = UNSET
        else:
            dataset_output = self.dataset_output

        external_id: Union[None, Unset, str]
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        feedback_rating_info: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.feedback_rating_info, Unset):
            feedback_rating_info = self.feedback_rating_info.to_dict()

        has_children: Union[None, Unset, bool]
        if isinstance(self.has_children, Unset):
            has_children = UNSET
        else:
            has_children = self.has_children

        input_ = self.input_

        is_complete = self.is_complete

        metric_info: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metric_info, Unset):
            metric_info = UNSET
        elif isinstance(self.metric_info, ExtendedTraceRecordWithChildrenMetricInfoType0):
            metric_info = self.metric_info.to_dict()
        else:
            metric_info = self.metric_info

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        metrics_batch_id: Union[None, Unset, str]
        if isinstance(self.metrics_batch_id, Unset):
            metrics_batch_id = UNSET
        else:
            metrics_batch_id = self.metrics_batch_id

        name = self.name

        output: Union[None, Unset, str]
        if isinstance(self.output, Unset):
            output = UNSET
        else:
            output = self.output

        redacted_input: Union[None, Unset, str]
        if isinstance(self.redacted_input, Unset):
            redacted_input = UNSET
        else:
            redacted_input = self.redacted_input

        redacted_output: Union[None, Unset, str]
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        else:
            redacted_output = self.redacted_output

        session_batch_id: Union[None, Unset, str]
        if isinstance(self.session_batch_id, Unset):
            session_batch_id = UNSET
        else:
            session_batch_id = self.session_batch_id

        spans: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.spans, Unset):
            spans = []
            for spans_item_data in self.spans:
                spans_item: dict[str, Any]
                if isinstance(spans_item_data, ExtendedAgentSpanRecordWithChildren):
                    spans_item = spans_item_data.to_dict()
                elif isinstance(spans_item_data, ExtendedWorkflowSpanRecordWithChildren):
                    spans_item = spans_item_data.to_dict()
                elif isinstance(spans_item_data, ExtendedLlmSpanRecord):
                    spans_item = spans_item_data.to_dict()
                elif isinstance(spans_item_data, ExtendedToolSpanRecordWithChildren):
                    spans_item = spans_item_data.to_dict()
                else:
                    spans_item = spans_item_data.to_dict()

                spans.append(spans_item)

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        type_ = self.type_

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        user_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "project_id": project_id, "run_id": run_id, "session_id": session_id, "trace_id": trace_id}
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if dataset_input is not UNSET:
            field_dict["dataset_input"] = dataset_input
        if dataset_metadata is not UNSET:
            field_dict["dataset_metadata"] = dataset_metadata
        if dataset_output is not UNSET:
            field_dict["dataset_output"] = dataset_output
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if feedback_rating_info is not UNSET:
            field_dict["feedback_rating_info"] = feedback_rating_info
        if has_children is not UNSET:
            field_dict["has_children"] = has_children
        if input_ is not UNSET:
            field_dict["input"] = input_
        if is_complete is not UNSET:
            field_dict["is_complete"] = is_complete
        if metric_info is not UNSET:
            field_dict["metric_info"] = metric_info
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if metrics_batch_id is not UNSET:
            field_dict["metrics_batch_id"] = metrics_batch_id
        if name is not UNSET:
            field_dict["name"] = name
        if output is not UNSET:
            field_dict["output"] = output
        if redacted_input is not UNSET:
            field_dict["redacted_input"] = redacted_input
        if redacted_output is not UNSET:
            field_dict["redacted_output"] = redacted_output
        if session_batch_id is not UNSET:
            field_dict["session_batch_id"] = session_batch_id
        if spans is not UNSET:
            field_dict["spans"] = spans
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type_ is not UNSET:
            field_dict["type"] = type_
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
        from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
        from ..models.extended_retriever_span_record_with_children import ExtendedRetrieverSpanRecordWithChildren
        from ..models.extended_tool_span_record_with_children import ExtendedToolSpanRecordWithChildren
        from ..models.extended_trace_record_with_children_dataset_metadata import (
            ExtendedTraceRecordWithChildrenDatasetMetadata,
        )
        from ..models.extended_trace_record_with_children_feedback_rating_info import (
            ExtendedTraceRecordWithChildrenFeedbackRatingInfo,
        )
        from ..models.extended_trace_record_with_children_metric_info_type_0 import (
            ExtendedTraceRecordWithChildrenMetricInfoType0,
        )
        from ..models.extended_trace_record_with_children_user_metadata import (
            ExtendedTraceRecordWithChildrenUserMetadata,
        )
        from ..models.extended_workflow_span_record_with_children import ExtendedWorkflowSpanRecordWithChildren
        from ..models.metrics import Metrics

        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        session_id = d.pop("session_id")

        trace_id = d.pop("trace_id")

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        def _parse_dataset_input(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_input = _parse_dataset_input(d.pop("dataset_input", UNSET))

        _dataset_metadata = d.pop("dataset_metadata", UNSET)
        dataset_metadata: Union[Unset, ExtendedTraceRecordWithChildrenDatasetMetadata]
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = ExtendedTraceRecordWithChildrenDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_dataset_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_output = _parse_dataset_output(d.pop("dataset_output", UNSET))

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        _feedback_rating_info = d.pop("feedback_rating_info", UNSET)
        feedback_rating_info: Union[Unset, ExtendedTraceRecordWithChildrenFeedbackRatingInfo]
        if isinstance(_feedback_rating_info, Unset):
            feedback_rating_info = UNSET
        else:
            feedback_rating_info = ExtendedTraceRecordWithChildrenFeedbackRatingInfo.from_dict(_feedback_rating_info)

        def _parse_has_children(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        has_children = _parse_has_children(d.pop("has_children", UNSET))

        input_ = d.pop("input", UNSET)

        is_complete = d.pop("is_complete", UNSET)

        def _parse_metric_info(data: object) -> Union["ExtendedTraceRecordWithChildrenMetricInfoType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_info_type_0 = ExtendedTraceRecordWithChildrenMetricInfoType0.from_dict(data)

                return metric_info_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ExtendedTraceRecordWithChildrenMetricInfoType0", None, Unset], data)

        metric_info = _parse_metric_info(d.pop("metric_info", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, Metrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = Metrics.from_dict(_metrics)

        def _parse_metrics_batch_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metrics_batch_id = _parse_metrics_batch_id(d.pop("metrics_batch_id", UNSET))

        name = d.pop("name", UNSET)

        def _parse_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output = _parse_output(d.pop("output", UNSET))

        def _parse_redacted_input(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        def _parse_redacted_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        def _parse_session_batch_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_batch_id = _parse_session_batch_id(d.pop("session_batch_id", UNSET))

        spans = []
        _spans = d.pop("spans", UNSET)
        for spans_item_data in _spans or []:

            def _parse_spans_item(
                data: object,
            ) -> Union[
                "ExtendedAgentSpanRecordWithChildren",
                "ExtendedLlmSpanRecord",
                "ExtendedRetrieverSpanRecordWithChildren",
                "ExtendedToolSpanRecordWithChildren",
                "ExtendedWorkflowSpanRecordWithChildren",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_0 = ExtendedAgentSpanRecordWithChildren.from_dict(data)

                    return spans_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_1 = ExtendedWorkflowSpanRecordWithChildren.from_dict(data)

                    return spans_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_2 = ExtendedLlmSpanRecord.from_dict(data)

                    return spans_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_3 = ExtendedToolSpanRecordWithChildren.from_dict(data)

                    return spans_item_type_3
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                spans_item_type_4 = ExtendedRetrieverSpanRecordWithChildren.from_dict(data)

                return spans_item_type_4

            spans_item = _parse_spans_item(spans_item_data)

            spans.append(spans_item)

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        type_ = cast(Union[Literal["trace"], Unset], d.pop("type", UNSET))
        if type_ != "trace" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'trace', got '{type_}'")

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
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
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Union[Unset, ExtendedTraceRecordWithChildrenUserMetadata]
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = ExtendedTraceRecordWithChildrenUserMetadata.from_dict(_user_metadata)

        extended_trace_record_with_children = cls(
            id=id,
            project_id=project_id,
            run_id=run_id,
            session_id=session_id,
            trace_id=trace_id,
            created_at=created_at,
            dataset_input=dataset_input,
            dataset_metadata=dataset_metadata,
            dataset_output=dataset_output,
            external_id=external_id,
            feedback_rating_info=feedback_rating_info,
            has_children=has_children,
            input_=input_,
            is_complete=is_complete,
            metric_info=metric_info,
            metrics=metrics,
            metrics_batch_id=metrics_batch_id,
            name=name,
            output=output,
            redacted_input=redacted_input,
            redacted_output=redacted_output,
            session_batch_id=session_batch_id,
            spans=spans,
            status_code=status_code,
            tags=tags,
            type_=type_,
            updated_at=updated_at,
            user_metadata=user_metadata,
        )

        extended_trace_record_with_children.additional_properties = d
        return extended_trace_record_with_children

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
