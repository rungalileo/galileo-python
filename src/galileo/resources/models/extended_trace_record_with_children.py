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
    Attributes
    ----------
        id (str): Galileo ID of the trace
        session_id (str): Galileo ID of the session containing the trace (or the same value as id for a trace)
        trace_id (str): Galileo ID of the trace containing the span (or the same value as id for a trace)
        project_id (str): Galileo ID of the project associated with this trace or span
        run_id (str): Galileo ID of the run (log stream or experiment) associated with this trace or span
        spans (Union[Unset, list[Union['ExtendedAgentSpanRecordWithChildren', 'ExtendedLlmSpanRecord',
            'ExtendedRetrieverSpanRecordWithChildren', 'ExtendedToolSpanRecordWithChildren',
            'ExtendedWorkflowSpanRecordWithChildren']]]):
        type_ (Union[Literal['trace'], Unset]): Type of the trace, span or session. Default: 'trace'.
        input_ (Union[Unset, str]): Input to the trace or span. Default: ''.
        redacted_input (Union[None, Unset, str]): Redacted input of the trace or span.
        output (Union[None, Unset, str]): Output of the trace or span.
        redacted_output (Union[None, Unset, str]): Redacted output of the trace or span.
        name (Union[Unset, str]): Name of the trace, span or session. Default: ''.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        user_metadata (Union[Unset, ExtendedTraceRecordWithChildrenUserMetadata]): Metadata associated with this trace
            or span.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        metrics (Union[Unset, Metrics]):
        external_id (Union[None, Unset, str]): A user-provided session, trace or span ID.
        dataset_input (Union[None, Unset, str]): Input to the dataset associated with this trace
        dataset_output (Union[None, Unset, str]): Output from the dataset associated with this trace
        dataset_metadata (Union[Unset, ExtendedTraceRecordWithChildrenDatasetMetadata]): Metadata from the dataset
            associated with this trace
        updated_at (Union[None, Unset, datetime.datetime]): Timestamp of the session or trace or span's last update
        has_children (Union[None, Unset, bool]): Whether or not this trace or span has child spans
        metrics_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        session_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        feedback_rating_info (Union[Unset, ExtendedTraceRecordWithChildrenFeedbackRatingInfo]): Feedback information
            related to the record
        metric_info (Union['ExtendedTraceRecordWithChildrenMetricInfoType0', None, Unset]): Detailed information about
            the metrics associated with this trace or span
        is_complete (Union[Unset, bool]): Whether the trace is complete or not Default: True.
        num_spans (Union[None, Unset, int]):
    """

    id: str
    session_id: str
    trace_id: str
    project_id: str
    run_id: str
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
    type_: Union[Literal["trace"], Unset] = "trace"
    input_: Union[Unset, str] = ""
    redacted_input: Union[None, Unset, str] = UNSET
    output: Union[None, Unset, str] = UNSET
    redacted_output: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = ""
    created_at: Union[Unset, datetime.datetime] = UNSET
    user_metadata: Union[Unset, "ExtendedTraceRecordWithChildrenUserMetadata"] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    dataset_input: Union[None, Unset, str] = UNSET
    dataset_output: Union[None, Unset, str] = UNSET
    dataset_metadata: Union[Unset, "ExtendedTraceRecordWithChildrenDatasetMetadata"] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    has_children: Union[None, Unset, bool] = UNSET
    metrics_batch_id: Union[None, Unset, str] = UNSET
    session_batch_id: Union[None, Unset, str] = UNSET
    feedback_rating_info: Union[Unset, "ExtendedTraceRecordWithChildrenFeedbackRatingInfo"] = UNSET
    metric_info: Union["ExtendedTraceRecordWithChildrenMetricInfoType0", None, Unset] = UNSET
    is_complete: Union[Unset, bool] = True
    num_spans: Union[None, Unset, int] = UNSET
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

        session_id = self.session_id

        trace_id = self.trace_id

        project_id = self.project_id

        run_id = self.run_id

        spans: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.spans, Unset):
            spans = []
            for spans_item_data in self.spans:
                spans_item: dict[str, Any]
                if isinstance(
                    spans_item_data,
                    (
                        ExtendedAgentSpanRecordWithChildren,
                        ExtendedWorkflowSpanRecordWithChildren,
                        ExtendedLlmSpanRecord,
                        ExtendedToolSpanRecordWithChildren,
                    ),
                ):
                    spans_item = spans_item_data.to_dict()
                else:
                    spans_item = spans_item_data.to_dict()

                spans.append(spans_item)

        type_ = self.type_

        input_ = self.input_

        redacted_input: Union[None, Unset, str]
        redacted_input = UNSET if isinstance(self.redacted_input, Unset) else self.redacted_input

        output: Union[None, Unset, str]
        output = UNSET if isinstance(self.output, Unset) else self.output

        redacted_output: Union[None, Unset, str]
        redacted_output = UNSET if isinstance(self.redacted_output, Unset) else self.redacted_output

        name = self.name

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        user_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        status_code: Union[None, Unset, int]
        status_code = UNSET if isinstance(self.status_code, Unset) else self.status_code

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        external_id: Union[None, Unset, str]
        external_id = UNSET if isinstance(self.external_id, Unset) else self.external_id

        dataset_input: Union[None, Unset, str]
        dataset_input = UNSET if isinstance(self.dataset_input, Unset) else self.dataset_input

        dataset_output: Union[None, Unset, str]
        dataset_output = UNSET if isinstance(self.dataset_output, Unset) else self.dataset_output

        dataset_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.dataset_metadata, Unset):
            dataset_metadata = self.dataset_metadata.to_dict()

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        has_children: Union[None, Unset, bool]
        has_children = UNSET if isinstance(self.has_children, Unset) else self.has_children

        metrics_batch_id: Union[None, Unset, str]
        metrics_batch_id = UNSET if isinstance(self.metrics_batch_id, Unset) else self.metrics_batch_id

        session_batch_id: Union[None, Unset, str]
        session_batch_id = UNSET if isinstance(self.session_batch_id, Unset) else self.session_batch_id

        feedback_rating_info: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.feedback_rating_info, Unset):
            feedback_rating_info = self.feedback_rating_info.to_dict()

        metric_info: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metric_info, Unset):
            metric_info = UNSET
        elif isinstance(self.metric_info, ExtendedTraceRecordWithChildrenMetricInfoType0):
            metric_info = self.metric_info.to_dict()
        else:
            metric_info = self.metric_info

        is_complete = self.is_complete

        num_spans: Union[None, Unset, int]
        num_spans = UNSET if isinstance(self.num_spans, Unset) else self.num_spans

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "session_id": session_id, "trace_id": trace_id, "project_id": project_id, "run_id": run_id}
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
        if metric_info is not UNSET:
            field_dict["metric_info"] = metric_info
        if is_complete is not UNSET:
            field_dict["is_complete"] = is_complete
        if num_spans is not UNSET:
            field_dict["num_spans"] = num_spans

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
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

        session_id = d.pop("session_id")

        trace_id = d.pop("trace_id")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

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
                # If we reach here, none of the parsers succeeded
                discriminator_info = f" (type={data.get('type')})" if isinstance(data, dict) and "type" in data else ""
                raise ValueError(f"Could not parse union type for spans_item{discriminator_info}")

            spans_item = _parse_spans_item(spans_item_data)

            spans.append(spans_item)

        type_ = cast(Union[Literal["trace"], Unset], d.pop("type", UNSET))
        if type_ != "trace" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'trace', got '{type_}'")

        input_ = d.pop("input", UNSET)

        def _parse_redacted_input(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        def _parse_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output = _parse_output(d.pop("output", UNSET))

        def _parse_redacted_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        created_at = UNSET if isinstance(_created_at, Unset) else isoparse(_created_at)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Union[Unset, ExtendedTraceRecordWithChildrenUserMetadata]
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = ExtendedTraceRecordWithChildrenUserMetadata.from_dict(_user_metadata)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, Metrics]
        metrics = UNSET if isinstance(_metrics, Unset) else Metrics.from_dict(_metrics)

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_dataset_input(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_input = _parse_dataset_input(d.pop("dataset_input", UNSET))

        def _parse_dataset_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_output = _parse_dataset_output(d.pop("dataset_output", UNSET))

        _dataset_metadata = d.pop("dataset_metadata", UNSET)
        dataset_metadata: Union[Unset, ExtendedTraceRecordWithChildrenDatasetMetadata]
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = ExtendedTraceRecordWithChildrenDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
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
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_has_children(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        has_children = _parse_has_children(d.pop("has_children", UNSET))

        def _parse_metrics_batch_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metrics_batch_id = _parse_metrics_batch_id(d.pop("metrics_batch_id", UNSET))

        def _parse_session_batch_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_batch_id = _parse_session_batch_id(d.pop("session_batch_id", UNSET))

        _feedback_rating_info = d.pop("feedback_rating_info", UNSET)
        feedback_rating_info: Union[Unset, ExtendedTraceRecordWithChildrenFeedbackRatingInfo]
        if isinstance(_feedback_rating_info, Unset):
            feedback_rating_info = UNSET
        else:
            feedback_rating_info = ExtendedTraceRecordWithChildrenFeedbackRatingInfo.from_dict(_feedback_rating_info)

        def _parse_metric_info(data: object) -> Union["ExtendedTraceRecordWithChildrenMetricInfoType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
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
                return ExtendedTraceRecordWithChildrenMetricInfoType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ExtendedTraceRecordWithChildrenMetricInfoType0", None, Unset], data)

        metric_info = _parse_metric_info(d.pop("metric_info", UNSET))

        is_complete = d.pop("is_complete", UNSET)

        def _parse_num_spans(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_spans = _parse_num_spans(d.pop("num_spans", UNSET))

        extended_trace_record_with_children = cls(
            id=id,
            session_id=session_id,
            trace_id=trace_id,
            project_id=project_id,
            run_id=run_id,
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
            updated_at=updated_at,
            has_children=has_children,
            metrics_batch_id=metrics_batch_id,
            session_batch_id=session_batch_id,
            feedback_rating_info=feedback_rating_info,
            metric_info=metric_info,
            is_complete=is_complete,
            num_spans=num_spans,
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
