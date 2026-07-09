from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_span import AgentSpan
    from ..models.control_span import ControlSpan
    from ..models.document import Document
    from ..models.llm_span import LlmSpan
    from ..models.metrics import Metrics
    from ..models.retriever_span_dataset_metadata import RetrieverSpanDatasetMetadata
    from ..models.retriever_span_user_metadata import RetrieverSpanUserMetadata
    from ..models.tool_span import ToolSpan
    from ..models.workflow_span import WorkflowSpan


T = TypeVar("T", bound="RetrieverSpan")


@_attrs_define
class RetrieverSpan:
    """
    Attributes:
        type_ (Literal['retriever'] | Unset): Type of the trace, span or session. Default: 'retriever'.
        input_ (str | Unset): Input to the trace or span. Default: ''.
        redacted_input (None | str | Unset): Redacted input of the trace or span.
        output (list[Document] | Unset): Output of the trace or span.
        redacted_output (list[Document] | None | Unset): Redacted output of the trace or span.
        name (str | Unset): Name of the trace, span or session. Default: ''.
        created_at (datetime.datetime | Unset): Timestamp of the trace or span's creation.
        user_metadata (RetrieverSpanUserMetadata | Unset): Metadata associated with this trace or span.
        tags (list[str] | Unset): Tags associated with this trace or span.
        status_code (int | None | Unset): Status code of the trace or span. Used for logging failure or error states.
        metrics (Metrics | Unset):
        external_id (None | str | Unset): A user-provided session, trace or span ID.
        dataset_input (None | str | Unset): Input to the dataset associated with this trace
        dataset_output (None | str | Unset): Output from the dataset associated with this trace
        dataset_metadata (RetrieverSpanDatasetMetadata | Unset): Metadata from the dataset associated with this trace
        id (None | str | Unset): Galileo ID of the session, trace or span
        session_id (None | str | Unset): Galileo ID of the session containing the trace or span or session
        trace_id (None | str | Unset): Galileo ID of the trace containing the span (or the same value as id for a trace)
        step_number (int | None | Unset): Topological step number of the span.
        parent_id (None | str | Unset): Galileo ID of the parent of this span
        spans (list[AgentSpan | ControlSpan | LlmSpan | RetrieverSpan | ToolSpan | WorkflowSpan] | Unset): Child spans.
    """

    type_: Literal["retriever"] | Unset = "retriever"
    input_: str | Unset = ""
    redacted_input: None | str | Unset = UNSET
    output: list[Document] | Unset = UNSET
    redacted_output: list[Document] | None | Unset = UNSET
    name: str | Unset = ""
    created_at: datetime.datetime | Unset = UNSET
    user_metadata: RetrieverSpanUserMetadata | Unset = UNSET
    tags: list[str] | Unset = UNSET
    status_code: int | None | Unset = UNSET
    metrics: Metrics | Unset = UNSET
    external_id: None | str | Unset = UNSET
    dataset_input: None | str | Unset = UNSET
    dataset_output: None | str | Unset = UNSET
    dataset_metadata: RetrieverSpanDatasetMetadata | Unset = UNSET
    id: None | str | Unset = UNSET
    session_id: None | str | Unset = UNSET
    trace_id: None | str | Unset = UNSET
    step_number: int | None | Unset = UNSET
    parent_id: None | str | Unset = UNSET
    spans: list[AgentSpan | ControlSpan | LlmSpan | RetrieverSpan | ToolSpan | WorkflowSpan] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_span import AgentSpan
        from ..models.llm_span import LlmSpan
        from ..models.tool_span import ToolSpan
        from ..models.workflow_span import WorkflowSpan

        type_ = self.type_

        input_ = self.input_

        redacted_input: None | str | Unset
        if isinstance(self.redacted_input, Unset):
            redacted_input = UNSET
        else:
            redacted_input = self.redacted_input

        output: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.output, Unset):
            output = []
            for output_item_data in self.output:
                output_item = output_item_data.to_dict()
                output.append(output_item)

        redacted_output: list[dict[str, Any]] | None | Unset
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        elif isinstance(self.redacted_output, list):
            redacted_output = []
            for redacted_output_type_0_item_data in self.redacted_output:
                redacted_output_type_0_item = redacted_output_type_0_item_data.to_dict()
                redacted_output.append(redacted_output_type_0_item)

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
        else:
            id = self.id

        session_id: None | str | Unset
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        else:
            session_id = self.session_id

        trace_id: None | str | Unset
        if isinstance(self.trace_id, Unset):
            trace_id = UNSET
        else:
            trace_id = self.trace_id

        step_number: int | None | Unset
        if isinstance(self.step_number, Unset):
            step_number = UNSET
        else:
            step_number = self.step_number

        parent_id: None | str | Unset
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        else:
            parent_id = self.parent_id

        spans: list[dict[str, Any]] | Unset = UNSET
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
                elif isinstance(spans_item_data, ToolSpan):
                    spans_item = spans_item_data.to_dict()
                else:
                    spans_item = spans_item_data.to_dict()

                spans.append(spans_item)

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_span import AgentSpan
        from ..models.control_span import ControlSpan
        from ..models.document import Document
        from ..models.llm_span import LlmSpan
        from ..models.metrics import Metrics
        from ..models.retriever_span_dataset_metadata import RetrieverSpanDatasetMetadata
        from ..models.retriever_span_user_metadata import RetrieverSpanUserMetadata
        from ..models.tool_span import ToolSpan
        from ..models.workflow_span import WorkflowSpan

        d = dict(src_dict)
        type_ = cast(Literal["retriever"] | Unset, d.pop("type", UNSET))
        if type_ != "retriever" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'retriever', got '{type_}'")

        input_ = d.pop("input", UNSET)

        def _parse_redacted_input(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        _output = d.pop("output", UNSET)
        output: list[Document] | Unset = UNSET
        if _output is not UNSET:
            output = []
            for output_item_data in _output:
                output_item = Document.from_dict(output_item_data)

                output.append(output_item)

        def _parse_redacted_output(data: object) -> list[Document] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_0 = []
                _redacted_output_type_0 = data
                for redacted_output_type_0_item_data in _redacted_output_type_0:
                    redacted_output_type_0_item = Document.from_dict(redacted_output_type_0_item_data)

                    redacted_output_type_0.append(redacted_output_type_0_item)

                return redacted_output_type_0
            except:  # noqa: E722
                pass
            return cast(list[Document] | None | Unset, data)

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: RetrieverSpanUserMetadata | Unset
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = RetrieverSpanUserMetadata.from_dict(_user_metadata)

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
        dataset_metadata: RetrieverSpanDatasetMetadata | Unset
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = RetrieverSpanDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_trace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trace_id = _parse_trace_id(d.pop("trace_id", UNSET))

        def _parse_step_number(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        step_number = _parse_step_number(d.pop("step_number", UNSET))

        def _parse_parent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_id = _parse_parent_id(d.pop("parent_id", UNSET))

        _spans = d.pop("spans", UNSET)
        spans: list[AgentSpan | ControlSpan | LlmSpan | RetrieverSpan | ToolSpan | WorkflowSpan] | Unset = UNSET
        if _spans is not UNSET:
            spans = []
            for spans_item_data in _spans:

                def _parse_spans_item(
                    data: object,
                ) -> AgentSpan | ControlSpan | LlmSpan | RetrieverSpan | ToolSpan | WorkflowSpan:
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
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        spans_item_type_4 = ToolSpan.from_dict(data)

                        return spans_item_type_4
                    except:  # noqa: E722
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_5 = ControlSpan.from_dict(data)

                    return spans_item_type_5

                spans_item = _parse_spans_item(spans_item_data)

                spans.append(spans_item)

        retriever_span = cls(
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
        )

        retriever_span.additional_properties = d
        return retriever_span

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
