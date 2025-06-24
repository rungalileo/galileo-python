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
    from ..models.tool_span import ToolSpan
    from ..models.trace_dataset_metadata import TraceDatasetMetadata
    from ..models.trace_user_metadata import TraceUserMetadata
    from ..models.workflow_span import WorkflowSpan


T = TypeVar("T", bound="Trace")


@_attrs_define
class Trace:
    """
    Attributes:
        input_ (str): Input to the trace or span.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        dataset_input (Union[None, Unset, str]): Input to the dataset associated with this trace
        dataset_metadata (Union[Unset, TraceDatasetMetadata]): Metadata from the dataset associated with this trace
        dataset_output (Union[None, Unset, str]): Output from the dataset associated with this trace
        external_id (Union[None, Unset, str]): A user-provided session, trace or span ID.
        id (Union[None, Unset, str]): Galileo ID of the session, trace or span
        metrics (Union[Unset, Metrics]):
        name (Union[Unset, str]): Name of the trace, span or session. Default: ''.
        output (Union[None, Unset, str]): Output of the trace or span.
        spans (Union[Unset, list[Union['AgentSpan', 'LlmSpan', 'RetrieverSpan', 'ToolSpan', 'WorkflowSpan']]]): Child
            spans.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        step_number (Union[None, Unset, int]): Topological step number of the span.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        type_ (Union[Literal['trace'], Unset]): Type of the trace, span or session. Default: 'trace'.
        user_metadata (Union[Unset, TraceUserMetadata]): Metadata associated with this trace or span.
    """

    input_: str
    created_at: Union[Unset, datetime.datetime] = UNSET
    dataset_input: Union[None, Unset, str] = UNSET
    dataset_metadata: Union[Unset, "TraceDatasetMetadata"] = UNSET
    dataset_output: Union[None, Unset, str] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    id: Union[None, Unset, str] = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    name: Union[Unset, str] = ""
    output: Union[None, Unset, str] = UNSET
    spans: Union[Unset, list[Union["AgentSpan", "LlmSpan", "RetrieverSpan", "ToolSpan", "WorkflowSpan"]]] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    step_number: Union[None, Unset, int] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    type_: Union[Literal["trace"], Unset] = "trace"
    user_metadata: Union[Unset, "TraceUserMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_span import AgentSpan
        from ..models.llm_span import LlmSpan
        from ..models.retriever_span import RetrieverSpan
        from ..models.workflow_span import WorkflowSpan

        input_ = self.input_

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

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        name = self.name

        output: Union[None, Unset, str]
        if isinstance(self.output, Unset):
            output = UNSET
        else:
            output = self.output

        spans: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.spans, Unset):
            spans = []
            for spans_item_data in self.spans:
                spans_item: dict[str, Any]
                if isinstance(spans_item_data, AgentSpan):
                    spans_item = spans_item_data.to_dict()
                elif isinstance(spans_item_data, WorkflowSpan):
                    spans_item = spans_item_data.to_dict()
                elif isinstance(spans_item_data, LlmSpan):
                    spans_item = spans_item_data.to_dict()
                elif isinstance(spans_item_data, RetrieverSpan):
                    spans_item = spans_item_data.to_dict()
                else:
                    spans_item = spans_item_data.to_dict()

                spans.append(spans_item)

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        step_number: Union[None, Unset, int]
        if isinstance(self.step_number, Unset):
            step_number = UNSET
        else:
            step_number = self.step_number

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        type_ = self.type_

        user_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_})
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
        if id is not UNSET:
            field_dict["id"] = id
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if name is not UNSET:
            field_dict["name"] = name
        if output is not UNSET:
            field_dict["output"] = output
        if spans is not UNSET:
            field_dict["spans"] = spans
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if step_number is not UNSET:
            field_dict["step_number"] = step_number
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_span import AgentSpan
        from ..models.llm_span import LlmSpan
        from ..models.metrics import Metrics
        from ..models.retriever_span import RetrieverSpan
        from ..models.tool_span import ToolSpan
        from ..models.trace_dataset_metadata import TraceDatasetMetadata
        from ..models.trace_user_metadata import TraceUserMetadata
        from ..models.workflow_span import WorkflowSpan

        d = dict(src_dict)
        input_ = d.pop("input")

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
        dataset_metadata: Union[Unset, TraceDatasetMetadata]
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = TraceDatasetMetadata.from_dict(_dataset_metadata)

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

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, Metrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = Metrics.from_dict(_metrics)

        name = d.pop("name", UNSET)

        def _parse_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output = _parse_output(d.pop("output", UNSET))

        spans = []
        _spans = d.pop("spans", UNSET)
        for spans_item_data in _spans or []:

            def _parse_spans_item(
                data: object,
            ) -> Union["AgentSpan", "LlmSpan", "RetrieverSpan", "ToolSpan", "WorkflowSpan"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_0 = AgentSpan.from_dict(data)

                    return spans_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_1 = WorkflowSpan.from_dict(data)

                    return spans_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_2 = LlmSpan.from_dict(data)

                    return spans_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_3 = RetrieverSpan.from_dict(data)

                    return spans_item_type_3
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                spans_item_type_4 = ToolSpan.from_dict(data)

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

        def _parse_step_number(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        step_number = _parse_step_number(d.pop("step_number", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        type_ = cast(Union[Literal["trace"], Unset], d.pop("type", UNSET))
        if type_ != "trace" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'trace', got '{type_}'")

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Union[Unset, TraceUserMetadata]
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = TraceUserMetadata.from_dict(_user_metadata)

        trace = cls(
            input_=input_,
            created_at=created_at,
            dataset_input=dataset_input,
            dataset_metadata=dataset_metadata,
            dataset_output=dataset_output,
            external_id=external_id,
            id=id,
            metrics=metrics,
            name=name,
            output=output,
            spans=spans,
            status_code=status_code,
            step_number=step_number,
            tags=tags,
            type_=type_,
            user_metadata=user_metadata,
        )

        trace.additional_properties = d
        return trace

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
