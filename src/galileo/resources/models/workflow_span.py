import datetime
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.llm_span import LlmSpan
    from ..models.message import Message
    from ..models.metrics import Metrics
    from ..models.retriever_span import RetrieverSpan
    from ..models.tool_span import ToolSpan
    from ..models.workflow_span_user_metadata import WorkflowSpanUserMetadata


T = TypeVar("T", bound="WorkflowSpan")


@_attrs_define
class WorkflowSpan:
    """
    Attributes:
        input_ (Union[list['Message'], str]): Input to the trace or span.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        metrics (Union[Unset, Metrics]):
        name (Union[Unset, str]): Name of the trace or span. Default: ''.
        output (Union['Message', None, Unset, list['Document'], str]): Output of the trace or span.
        spans (Union[Unset, list[Union['LlmSpan', 'RetrieverSpan', 'ToolSpan', 'WorkflowSpan']]]): Child spans.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        type_ (Union[Literal['workflow'], Unset]): Type of the trace or span. Default: 'workflow'.
        user_metadata (Union[Unset, WorkflowSpanUserMetadata]): Metadata associated with this trace or span.
    """

    input_: Union[list["Message"], str]
    created_at: Union[Unset, datetime.datetime] = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    name: Union[Unset, str] = ""
    output: Union["Message", None, Unset, list["Document"], str] = UNSET
    spans: Union[Unset, list[Union["LlmSpan", "RetrieverSpan", "ToolSpan", "WorkflowSpan"]]] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    type_: Union[Literal["workflow"], Unset] = "workflow"
    user_metadata: Union[Unset, "WorkflowSpanUserMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.llm_span import LlmSpan
        from ..models.message import Message
        from ..models.retriever_span import RetrieverSpan

        input_: Union[list[dict[str, Any]], str]
        if isinstance(self.input_, list):
            input_ = []
            for input_type_1_item_data in self.input_:
                input_type_1_item = input_type_1_item_data.to_dict()
                input_.append(input_type_1_item)

        else:
            input_ = self.input_

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        name = self.name

        output: Union[None, Unset, dict[str, Any], list[dict[str, Any]], str]
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, Message):
            output = self.output.to_dict()
        elif isinstance(self.output, list):
            output = []
            for output_type_2_item_data in self.output:
                output_type_2_item = output_type_2_item_data.to_dict()
                output.append(output_type_2_item)

        else:
            output = self.output

        spans: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.spans, Unset):
            spans = []
            for spans_item_data in self.spans:
                spans_item: dict[str, Any]
                if isinstance(spans_item_data, WorkflowSpan):
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
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document import Document
        from ..models.llm_span import LlmSpan
        from ..models.message import Message
        from ..models.metrics import Metrics
        from ..models.retriever_span import RetrieverSpan
        from ..models.tool_span import ToolSpan
        from ..models.workflow_span_user_metadata import WorkflowSpanUserMetadata

        d = src_dict.copy()

        def _parse_input_(data: object) -> Union[list["Message"], str]:
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
            return cast(Union[list["Message"], str], data)

        input_ = _parse_input_(d.pop("input"))

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, Metrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = Metrics.from_dict(_metrics)

        name = d.pop("name", UNSET)

        def _parse_output(data: object) -> Union["Message", None, Unset, list["Document"], str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_1 = Message.from_dict(data)

                return output_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_2 = []
                _output_type_2 = data
                for output_type_2_item_data in _output_type_2:
                    output_type_2_item = Document.from_dict(output_type_2_item_data)

                    output_type_2.append(output_type_2_item)

                return output_type_2
            except:  # noqa: E722
                pass
            return cast(Union["Message", None, Unset, list["Document"], str], data)

        output = _parse_output(d.pop("output", UNSET))

        spans = []
        _spans = d.pop("spans", UNSET)
        for spans_item_data in _spans or []:

            def _parse_spans_item(data: object) -> Union["LlmSpan", "RetrieverSpan", "ToolSpan", "WorkflowSpan"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_0 = WorkflowSpan.from_dict(data)

                    return spans_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_1 = LlmSpan.from_dict(data)

                    return spans_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_2 = RetrieverSpan.from_dict(data)

                    return spans_item_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                spans_item_type_3 = ToolSpan.from_dict(data)

                return spans_item_type_3

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

        type_ = cast(Union[Literal["workflow"], Unset], d.pop("type", UNSET))
        if type_ != "workflow" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'workflow', got '{type_}'")

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Union[Unset, WorkflowSpanUserMetadata]
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = WorkflowSpanUserMetadata.from_dict(_user_metadata)

        workflow_span = cls(
            input_=input_,
            created_at=created_at,
            metrics=metrics,
            name=name,
            output=output,
            spans=spans,
            status_code=status_code,
            tags=tags,
            type_=type_,
            user_metadata=user_metadata,
        )

        workflow_span.additional_properties = d
        return workflow_span

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
