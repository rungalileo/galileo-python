import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_span import AgentSpan
    from ..models.llm_span import LlmSpan
    from ..models.metrics import Metrics
    from ..models.retriever_span import RetrieverSpan
    from ..models.tool_span_dataset_metadata import ToolSpanDatasetMetadata
    from ..models.tool_span_user_metadata import ToolSpanUserMetadata
    from ..models.workflow_span import WorkflowSpan


T = TypeVar("T", bound="ToolSpan")


@_attrs_define
class ToolSpan:
    """
    Attributes
    ----------
        type_ (Union[Literal['tool'], Unset]): Type of the trace, span or session. Default: 'tool'.
        input_ (Union[Unset, str]): Input to the trace or span. Default: ''.
        redacted_input (Union[None, Unset, str]): Redacted input of the trace or span.
        output (Union[None, Unset, str]): Output of the trace or span.
        redacted_output (Union[None, Unset, str]): Redacted output of the trace or span.
        name (Union[Unset, str]): Name of the trace, span or session. Default: ''.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        user_metadata (Union[Unset, ToolSpanUserMetadata]): Metadata associated with this trace or span.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        metrics (Union[Unset, Metrics]):
        external_id (Union[None, Unset, str]): A user-provided session, trace or span ID.
        dataset_input (Union[None, Unset, str]): Input to the dataset associated with this trace
        dataset_output (Union[None, Unset, str]): Output from the dataset associated with this trace
        dataset_metadata (Union[Unset, ToolSpanDatasetMetadata]): Metadata from the dataset associated with this trace
        id (Union[None, Unset, str]): Galileo ID of the session, trace or span
        session_id (Union[None, Unset, str]): Galileo ID of the session containing the trace or span or session
        trace_id (Union[None, Unset, str]): Galileo ID of the trace containing the span (or the same value as id for a
            trace)
        step_number (Union[None, Unset, int]): Topological step number of the span.
        parent_id (Union[None, Unset, str]): Galileo ID of the parent of this span
        spans (Union[Unset, list[Union['AgentSpan', 'LlmSpan', 'RetrieverSpan', 'ToolSpan', 'WorkflowSpan']]]): Child
            spans.
        tool_call_id (Union[None, Unset, str]): ID of the tool call.
    """

    type_: Union[Literal["tool"], Unset] = "tool"
    input_: Union[Unset, str] = ""
    redacted_input: Union[None, Unset, str] = UNSET
    output: Union[None, Unset, str] = UNSET
    redacted_output: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = ""
    created_at: Union[Unset, datetime.datetime] = UNSET
    user_metadata: Union[Unset, "ToolSpanUserMetadata"] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    dataset_input: Union[None, Unset, str] = UNSET
    dataset_output: Union[None, Unset, str] = UNSET
    dataset_metadata: Union[Unset, "ToolSpanDatasetMetadata"] = UNSET
    id: Union[None, Unset, str] = UNSET
    session_id: Union[None, Unset, str] = UNSET
    trace_id: Union[None, Unset, str] = UNSET
    step_number: Union[None, Unset, int] = UNSET
    parent_id: Union[None, Unset, str] = UNSET
    spans: Union[Unset, list[Union["AgentSpan", "LlmSpan", "RetrieverSpan", "ToolSpan", "WorkflowSpan"]]] = UNSET
    tool_call_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_span import AgentSpan
        from ..models.llm_span import LlmSpan
        from ..models.retriever_span import RetrieverSpan
        from ..models.workflow_span import WorkflowSpan

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

        id: Union[None, Unset, str]
        id = UNSET if isinstance(self.id, Unset) else self.id

        session_id: Union[None, Unset, str]
        session_id = UNSET if isinstance(self.session_id, Unset) else self.session_id

        trace_id: Union[None, Unset, str]
        trace_id = UNSET if isinstance(self.trace_id, Unset) else self.trace_id

        step_number: Union[None, Unset, int]
        step_number = UNSET if isinstance(self.step_number, Unset) else self.step_number

        parent_id: Union[None, Unset, str]
        parent_id = UNSET if isinstance(self.parent_id, Unset) else self.parent_id

        spans: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.spans, Unset):
            spans = []
            for spans_item_data in self.spans:
                spans_item: dict[str, Any]
                if isinstance(spans_item_data, (AgentSpan, WorkflowSpan, LlmSpan, RetrieverSpan)):
                    spans_item = spans_item_data.to_dict()
                else:
                    spans_item = spans_item_data.to_dict()

                spans.append(spans_item)

        tool_call_id: Union[None, Unset, str]
        tool_call_id = UNSET if isinstance(self.tool_call_id, Unset) else self.tool_call_id

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
        if step_number is not UNSET:
            field_dict["step_number"] = step_number
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if spans is not UNSET:
            field_dict["spans"] = spans
        if tool_call_id is not UNSET:
            field_dict["tool_call_id"] = tool_call_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_span import AgentSpan
        from ..models.llm_span import LlmSpan
        from ..models.metrics import Metrics
        from ..models.retriever_span import RetrieverSpan
        from ..models.tool_span_dataset_metadata import ToolSpanDatasetMetadata
        from ..models.tool_span_user_metadata import ToolSpanUserMetadata
        from ..models.workflow_span import WorkflowSpan

        d = dict(src_dict)
        type_ = cast(Union[Literal["tool"], Unset], d.pop("type", UNSET))
        if type_ != "tool" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'tool', got '{type_}'")

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
        user_metadata: Union[Unset, ToolSpanUserMetadata]
        user_metadata = UNSET if isinstance(_user_metadata, Unset) else ToolSpanUserMetadata.from_dict(_user_metadata)

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
        dataset_metadata: Union[Unset, ToolSpanDatasetMetadata]
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = ToolSpanDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_session_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_trace_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        trace_id = _parse_trace_id(d.pop("trace_id", UNSET))

        def _parse_step_number(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        step_number = _parse_step_number(d.pop("step_number", UNSET))

        def _parse_parent_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent_id = _parse_parent_id(d.pop("parent_id", UNSET))

        spans = []
        _spans = d.pop("spans", UNSET)
        for spans_item_data in _spans or []:

            def _parse_spans_item(
                data: object,
            ) -> Union["AgentSpan", "LlmSpan", "RetrieverSpan", "ToolSpan", "WorkflowSpan"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return AgentSpan.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return WorkflowSpan.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LlmSpan.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return RetrieverSpan.from_dict(data)

                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                return ToolSpan.from_dict(data)

            spans_item = _parse_spans_item(spans_item_data)

            spans.append(spans_item)

        def _parse_tool_call_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tool_call_id = _parse_tool_call_id(d.pop("tool_call_id", UNSET))

        tool_span = cls(
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
            step_number=step_number,
            parent_id=parent_id,
            spans=spans,
            tool_call_id=tool_call_id,
        )

        tool_span.additional_properties = d
        return tool_span

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
