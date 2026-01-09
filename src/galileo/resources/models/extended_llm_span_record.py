import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extended_llm_span_record_dataset_metadata import ExtendedLlmSpanRecordDatasetMetadata
    from ..models.extended_llm_span_record_feedback_rating_info import ExtendedLlmSpanRecordFeedbackRatingInfo
    from ..models.extended_llm_span_record_metric_info_type_0 import ExtendedLlmSpanRecordMetricInfoType0
    from ..models.extended_llm_span_record_tools_type_0_item import ExtendedLlmSpanRecordToolsType0Item
    from ..models.extended_llm_span_record_user_metadata import ExtendedLlmSpanRecordUserMetadata
    from ..models.image_generation_event import ImageGenerationEvent
    from ..models.internal_tool_call import InternalToolCall
    from ..models.llm_metrics import LlmMetrics
    from ..models.mcp_approval_request_event import MCPApprovalRequestEvent
    from ..models.mcp_call_event import MCPCallEvent
    from ..models.mcp_list_tools_event import MCPListToolsEvent
    from ..models.message import Message
    from ..models.message_event import MessageEvent
    from ..models.reasoning_event import ReasoningEvent


T = TypeVar("T", bound="ExtendedLlmSpanRecord")


@_attrs_define
class ExtendedLlmSpanRecord:
    """
    Attributes
    ----------
        id (str): Galileo ID of the session, trace or span
        session_id (str): Galileo ID of the session containing the trace (or the same value as id for a trace)
        project_id (str): Galileo ID of the project associated with this trace or span
        run_id (str): Galileo ID of the run (log stream or experiment) associated with this trace or span
        parent_id (str): Galileo ID of the parent of this span
        type_ (Union[Literal['llm'], Unset]): Type of the trace, span or session. Default: 'llm'.
        input_ (Union[Unset, list['Message']]): Input to the trace or span.
        redacted_input (Union[None, Unset, list['Message']]): Redacted input of the trace or span.
        output (Union[Unset, Message]):
        redacted_output (Union['Message', None, Unset]): Redacted output of the trace or span.
        name (Union[Unset, str]): Name of the trace, span or session. Default: ''.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        user_metadata (Union[Unset, ExtendedLlmSpanRecordUserMetadata]): Metadata associated with this trace or span.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        metrics (Union[Unset, LlmMetrics]):
        external_id (Union[None, Unset, str]): A user-provided session, trace or span ID.
        dataset_input (Union[None, Unset, str]): Input to the dataset associated with this trace
        dataset_output (Union[None, Unset, str]): Output from the dataset associated with this trace
        dataset_metadata (Union[Unset, ExtendedLlmSpanRecordDatasetMetadata]): Metadata from the dataset associated with
            this trace
        trace_id (Union[None, Unset, str]): Galileo ID of the trace containing the span (or the same value as id for a
            trace)
        updated_at (Union[None, Unset, datetime.datetime]): Timestamp of the session or trace or span's last update
        has_children (Union[None, Unset, bool]): Whether or not this trace or span has child spans
        metrics_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        session_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        feedback_rating_info (Union[Unset, ExtendedLlmSpanRecordFeedbackRatingInfo]): Feedback information related to
            the record
        metric_info (Union['ExtendedLlmSpanRecordMetricInfoType0', None, Unset]): Detailed information about the metrics
            associated with this trace or span
        is_complete (Union[Unset, bool]): Whether the parent trace is complete or not Default: True.
        step_number (Union[None, Unset, int]): Topological step number of the span.
        tools (Union[None, Unset, list['ExtendedLlmSpanRecordToolsType0Item']]): List of available tools passed to the
            LLM on invocation.
        events (Union[None, Unset, list[Union['ImageGenerationEvent', 'InternalToolCall', 'MCPApprovalRequestEvent',
            'MCPCallEvent', 'MCPListToolsEvent', 'MessageEvent', 'ReasoningEvent']]]): List of reasoning, internal tool
            call, or MCP events that occurred during the LLM span.
        model (Union[None, Unset, str]): Model used for this span.
        temperature (Union[None, Unset, float]): Temperature used for generation.
        finish_reason (Union[None, Unset, str]): Reason for finishing.
    """

    id: str
    session_id: str
    project_id: str
    run_id: str
    parent_id: str
    type_: Union[Literal["llm"], Unset] = "llm"
    input_: Union[Unset, list["Message"]] = UNSET
    redacted_input: Union[None, Unset, list["Message"]] = UNSET
    output: Union[Unset, "Message"] = UNSET
    redacted_output: Union["Message", None, Unset] = UNSET
    name: Union[Unset, str] = ""
    created_at: Union[Unset, datetime.datetime] = UNSET
    user_metadata: Union[Unset, "ExtendedLlmSpanRecordUserMetadata"] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    metrics: Union[Unset, "LlmMetrics"] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    dataset_input: Union[None, Unset, str] = UNSET
    dataset_output: Union[None, Unset, str] = UNSET
    dataset_metadata: Union[Unset, "ExtendedLlmSpanRecordDatasetMetadata"] = UNSET
    trace_id: Union[None, Unset, str] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    has_children: Union[None, Unset, bool] = UNSET
    metrics_batch_id: Union[None, Unset, str] = UNSET
    session_batch_id: Union[None, Unset, str] = UNSET
    feedback_rating_info: Union[Unset, "ExtendedLlmSpanRecordFeedbackRatingInfo"] = UNSET
    metric_info: Union["ExtendedLlmSpanRecordMetricInfoType0", None, Unset] = UNSET
    is_complete: Union[Unset, bool] = True
    step_number: Union[None, Unset, int] = UNSET
    tools: Union[None, Unset, list["ExtendedLlmSpanRecordToolsType0Item"]] = UNSET
    events: Union[
        None,
        Unset,
        list[
            Union[
                "ImageGenerationEvent",
                "InternalToolCall",
                "MCPApprovalRequestEvent",
                "MCPCallEvent",
                "MCPListToolsEvent",
                "MessageEvent",
                "ReasoningEvent",
            ]
        ],
    ] = UNSET
    model: Union[None, Unset, str] = UNSET
    temperature: Union[None, Unset, float] = UNSET
    finish_reason: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.extended_llm_span_record_metric_info_type_0 import ExtendedLlmSpanRecordMetricInfoType0
        from ..models.image_generation_event import ImageGenerationEvent
        from ..models.internal_tool_call import InternalToolCall
        from ..models.mcp_call_event import MCPCallEvent
        from ..models.mcp_list_tools_event import MCPListToolsEvent
        from ..models.message import Message
        from ..models.message_event import MessageEvent
        from ..models.reasoning_event import ReasoningEvent

        id = self.id

        session_id = self.session_id

        project_id = self.project_id

        run_id = self.run_id

        parent_id = self.parent_id

        type_ = self.type_

        input_: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.input_, Unset):
            input_ = []
            for input_item_data in self.input_:
                input_item = input_item_data.to_dict()
                input_.append(input_item)

        redacted_input: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.redacted_input, Unset):
            redacted_input = UNSET
        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_0_item_data in self.redacted_input:
                redacted_input_type_0_item = redacted_input_type_0_item_data.to_dict()
                redacted_input.append(redacted_input_type_0_item)

        else:
            redacted_input = self.redacted_input

        output: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        redacted_output: Union[None, Unset, dict[str, Any]]
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        elif isinstance(self.redacted_output, Message):
            redacted_output = self.redacted_output.to_dict()
        else:
            redacted_output = self.redacted_output

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

        trace_id: Union[None, Unset, str]
        trace_id = UNSET if isinstance(self.trace_id, Unset) else self.trace_id

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
        elif isinstance(self.metric_info, ExtendedLlmSpanRecordMetricInfoType0):
            metric_info = self.metric_info.to_dict()
        else:
            metric_info = self.metric_info

        is_complete = self.is_complete

        step_number: Union[None, Unset, int]
        step_number = UNSET if isinstance(self.step_number, Unset) else self.step_number

        tools: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)

        else:
            tools = self.tools

        events: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.events, Unset):
            events = UNSET
        elif isinstance(self.events, list):
            events = []
            for events_type_0_item_data in self.events:
                events_type_0_item: dict[str, Any]
                if isinstance(
                    events_type_0_item_data,
                    (
                        MessageEvent,
                        ReasoningEvent,
                        InternalToolCall,
                        ImageGenerationEvent,
                        MCPCallEvent,
                        MCPListToolsEvent,
                    ),
                ):
                    events_type_0_item = events_type_0_item_data.to_dict()
                else:
                    events_type_0_item = events_type_0_item_data.to_dict()

                events.append(events_type_0_item)

        else:
            events = self.events

        model: Union[None, Unset, str]
        model = UNSET if isinstance(self.model, Unset) else self.model

        temperature: Union[None, Unset, float]
        temperature = UNSET if isinstance(self.temperature, Unset) else self.temperature

        finish_reason: Union[None, Unset, str]
        finish_reason = UNSET if isinstance(self.finish_reason, Unset) else self.finish_reason

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
        if metric_info is not UNSET:
            field_dict["metric_info"] = metric_info
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
        from ..models.extended_llm_span_record_dataset_metadata import ExtendedLlmSpanRecordDatasetMetadata
        from ..models.extended_llm_span_record_feedback_rating_info import ExtendedLlmSpanRecordFeedbackRatingInfo
        from ..models.extended_llm_span_record_metric_info_type_0 import ExtendedLlmSpanRecordMetricInfoType0
        from ..models.extended_llm_span_record_tools_type_0_item import ExtendedLlmSpanRecordToolsType0Item
        from ..models.extended_llm_span_record_user_metadata import ExtendedLlmSpanRecordUserMetadata
        from ..models.image_generation_event import ImageGenerationEvent
        from ..models.internal_tool_call import InternalToolCall
        from ..models.llm_metrics import LlmMetrics
        from ..models.mcp_approval_request_event import MCPApprovalRequestEvent
        from ..models.mcp_call_event import MCPCallEvent
        from ..models.mcp_list_tools_event import MCPListToolsEvent
        from ..models.message import Message
        from ..models.message_event import MessageEvent
        from ..models.reasoning_event import ReasoningEvent

        d = dict(src_dict)
        id = d.pop("id")

        session_id = d.pop("session_id")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        parent_id = d.pop("parent_id")

        type_ = cast(Union[Literal["llm"], Unset], d.pop("type", UNSET))
        if type_ != "llm" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'llm', got '{type_}'")

        input_ = []
        _input_ = d.pop("input", UNSET)
        for input_item_data in _input_ or []:
            input_item = Message.from_dict(input_item_data)

            input_.append(input_item)

        def _parse_redacted_input(data: object) -> Union[None, Unset, list["Message"]]:
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
            return cast(Union[None, Unset, list["Message"]], data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        _output = d.pop("output", UNSET)
        output: Union[Unset, Message]
        output = UNSET if isinstance(_output, Unset) else Message.from_dict(_output)

        def _parse_redacted_output(data: object) -> Union["Message", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Message.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["Message", None, Unset], data)

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        created_at = UNSET if isinstance(_created_at, Unset) else isoparse(_created_at)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Union[Unset, ExtendedLlmSpanRecordUserMetadata]
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = ExtendedLlmSpanRecordUserMetadata.from_dict(_user_metadata)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, LlmMetrics]
        metrics = UNSET if isinstance(_metrics, Unset) else LlmMetrics.from_dict(_metrics)

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
        dataset_metadata: Union[Unset, ExtendedLlmSpanRecordDatasetMetadata]
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = ExtendedLlmSpanRecordDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_trace_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        trace_id = _parse_trace_id(d.pop("trace_id", UNSET))

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
        feedback_rating_info: Union[Unset, ExtendedLlmSpanRecordFeedbackRatingInfo]
        if isinstance(_feedback_rating_info, Unset):
            feedback_rating_info = UNSET
        else:
            feedback_rating_info = ExtendedLlmSpanRecordFeedbackRatingInfo.from_dict(_feedback_rating_info)

        def _parse_metric_info(data: object) -> Union["ExtendedLlmSpanRecordMetricInfoType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExtendedLlmSpanRecordMetricInfoType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ExtendedLlmSpanRecordMetricInfoType0", None, Unset], data)

        metric_info = _parse_metric_info(d.pop("metric_info", UNSET))

        is_complete = d.pop("is_complete", UNSET)

        def _parse_step_number(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        step_number = _parse_step_number(d.pop("step_number", UNSET))

        def _parse_tools(data: object) -> Union[None, Unset, list["ExtendedLlmSpanRecordToolsType0Item"]]:
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
                    tools_type_0_item = ExtendedLlmSpanRecordToolsType0Item.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["ExtendedLlmSpanRecordToolsType0Item"]], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_events(
            data: object,
        ) -> Union[
            None,
            Unset,
            list[
                Union[
                    "ImageGenerationEvent",
                    "InternalToolCall",
                    "MCPApprovalRequestEvent",
                    "MCPCallEvent",
                    "MCPListToolsEvent",
                    "MessageEvent",
                    "ReasoningEvent",
                ]
            ],
        ]:
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
                    ) -> Union[
                        "ImageGenerationEvent",
                        "InternalToolCall",
                        "MCPApprovalRequestEvent",
                        "MCPCallEvent",
                        "MCPListToolsEvent",
                        "MessageEvent",
                        "ReasoningEvent",
                    ]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return MessageEvent.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return ReasoningEvent.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return InternalToolCall.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return ImageGenerationEvent.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return MCPCallEvent.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return MCPListToolsEvent.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return MCPApprovalRequestEvent.from_dict(data)

                    events_type_0_item = _parse_events_type_0_item(events_type_0_item_data)

                    events_type_0.append(events_type_0_item)

                return events_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    Unset,
                    list[
                        Union[
                            "ImageGenerationEvent",
                            "InternalToolCall",
                            "MCPApprovalRequestEvent",
                            "MCPCallEvent",
                            "MCPListToolsEvent",
                            "MessageEvent",
                            "ReasoningEvent",
                        ]
                    ],
                ],
                data,
            )

        events = _parse_events(d.pop("events", UNSET))

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_finish_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        finish_reason = _parse_finish_reason(d.pop("finish_reason", UNSET))

        extended_llm_span_record = cls(
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
            metric_info=metric_info,
            is_complete=is_complete,
            step_number=step_number,
            tools=tools,
            events=events,
            model=model,
            temperature=temperature,
            finish_reason=finish_reason,
        )

        extended_llm_span_record.additional_properties = d
        return extended_llm_span_record

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
