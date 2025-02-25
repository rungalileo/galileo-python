from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.llm_span import LlmSpan
    from ..models.message import Message
    from ..models.retriever_span import RetrieverSpan
    from ..models.step_with_child_spans import StepWithChildSpans
    from ..models.tool_span import ToolSpan
    from ..models.workflow_span_input_type_3 import WorkflowSpanInputType3
    from ..models.workflow_span_input_type_7_item import WorkflowSpanInputType7Item
    from ..models.workflow_span_input_type_8_item import WorkflowSpanInputType8Item
    from ..models.workflow_span_metadata import WorkflowSpanMetadata
    from ..models.workflow_span_output_type_3 import WorkflowSpanOutputType3
    from ..models.workflow_span_output_type_7_item import WorkflowSpanOutputType7Item
    from ..models.workflow_span_output_type_8_item import WorkflowSpanOutputType8Item


T = TypeVar("T", bound="WorkflowSpan")


@_attrs_define
class WorkflowSpan:
    """
    Attributes:
        input_ (Union['Document', 'Message', 'WorkflowSpanInputType3', list['Document'], list['Message'],
            list['WorkflowSpanInputType7Item'], list['WorkflowSpanInputType8Item'], list[str], str]): Input to the step.
        created_at_ns (Union[Unset, int]): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (Union[Unset, int]): Duration of the step in nanoseconds. Default: 0.
        ground_truth (Union[None, Unset, str]): Ground truth expected output for the step.
        metadata (Union[Unset, WorkflowSpanMetadata]): Metadata associated with this step.
        name (Union[Unset, str]): Name of the step. Default: ''.
        output (Union['Document', 'Message', 'WorkflowSpanOutputType3', Unset, list['Document'], list['Message'],
            list['WorkflowSpanOutputType7Item'], list['WorkflowSpanOutputType8Item'], list[str], str]): Output of the step.
            Default: ''.
        parent (Union['StepWithChildSpans', None, Unset]): Parent node of the current node. For internal use only.
        spans (Union[Unset, list[Union['LlmSpan', 'RetrieverSpan', 'ToolSpan', 'WorkflowSpan']]]): Child spans.
        status_code (Union[None, Unset, int]): Status code of the step. Used for logging failed/errored steps.
        type_ (Union[Literal['workflow'], Unset]): Type of the span. By default, it is set to workflow. Default:
            'workflow'.
    """

    input_: Union[
        "Document",
        "Message",
        "WorkflowSpanInputType3",
        list["Document"],
        list["Message"],
        list["WorkflowSpanInputType7Item"],
        list["WorkflowSpanInputType8Item"],
        list[str],
        str,
    ]
    created_at_ns: Union[Unset, int] = UNSET
    duration_ns: Union[Unset, int] = 0
    ground_truth: Union[None, Unset, str] = UNSET
    metadata: Union[Unset, "WorkflowSpanMetadata"] = UNSET
    name: Union[Unset, str] = ""
    output: Union[
        "Document",
        "Message",
        "WorkflowSpanOutputType3",
        Unset,
        list["Document"],
        list["Message"],
        list["WorkflowSpanOutputType7Item"],
        list["WorkflowSpanOutputType8Item"],
        list[str],
        str,
    ] = ""
    parent: Union["StepWithChildSpans", None, Unset] = UNSET
    spans: Union[Unset, list[Union["LlmSpan", "RetrieverSpan", "ToolSpan", "WorkflowSpan"]]] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    type_: Union[Literal["workflow"], Unset] = "workflow"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.document import Document
        from ..models.llm_span import LlmSpan
        from ..models.message import Message
        from ..models.retriever_span import RetrieverSpan
        from ..models.step_with_child_spans import StepWithChildSpans
        from ..models.workflow_span_input_type_3 import WorkflowSpanInputType3
        from ..models.workflow_span_output_type_3 import WorkflowSpanOutputType3

        input_: Union[dict[str, Any], list[dict[str, Any]], list[str], str]
        if isinstance(self.input_, Document):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, Message):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, WorkflowSpanInputType3):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, list):
            input_ = self.input_

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_5_item_data in self.input_:
                input_type_5_item = input_type_5_item_data.to_dict()
                input_.append(input_type_5_item)

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_6_item_data in self.input_:
                input_type_6_item = input_type_6_item_data.to_dict()
                input_.append(input_type_6_item)

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_7_item_data in self.input_:
                input_type_7_item = input_type_7_item_data.to_dict()
                input_.append(input_type_7_item)

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_8_item_data in self.input_:
                input_type_8_item = input_type_8_item_data.to_dict()
                input_.append(input_type_8_item)

        else:
            input_ = self.input_

        created_at_ns = self.created_at_ns

        duration_ns = self.duration_ns

        ground_truth: Union[None, Unset, str]
        if isinstance(self.ground_truth, Unset):
            ground_truth = UNSET
        else:
            ground_truth = self.ground_truth

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        name = self.name

        output: Union[Unset, dict[str, Any], list[dict[str, Any]], list[str], str]
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, Document):
            output = self.output.to_dict()
        elif isinstance(self.output, Message):
            output = self.output.to_dict()
        elif isinstance(self.output, WorkflowSpanOutputType3):
            output = self.output.to_dict()
        elif isinstance(self.output, list):
            output = self.output

        elif isinstance(self.output, list):
            output = []
            for output_type_5_item_data in self.output:
                output_type_5_item = output_type_5_item_data.to_dict()
                output.append(output_type_5_item)

        elif isinstance(self.output, list):
            output = []
            for output_type_6_item_data in self.output:
                output_type_6_item = output_type_6_item_data.to_dict()
                output.append(output_type_6_item)

        elif isinstance(self.output, list):
            output = []
            for output_type_7_item_data in self.output:
                output_type_7_item = output_type_7_item_data.to_dict()
                output.append(output_type_7_item)

        elif isinstance(self.output, list):
            output = []
            for output_type_8_item_data in self.output:
                output_type_8_item = output_type_8_item_data.to_dict()
                output.append(output_type_8_item)

        else:
            output = self.output

        parent: Union[None, Unset, dict[str, Any]]
        if isinstance(self.parent, Unset):
            parent = UNSET
        elif isinstance(self.parent, StepWithChildSpans):
            parent = self.parent.to_dict()
        else:
            parent = self.parent

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

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_})
        if created_at_ns is not UNSET:
            field_dict["created_at_ns"] = created_at_ns
        if duration_ns is not UNSET:
            field_dict["duration_ns"] = duration_ns
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if name is not UNSET:
            field_dict["name"] = name
        if output is not UNSET:
            field_dict["output"] = output
        if parent is not UNSET:
            field_dict["parent"] = parent
        if spans is not UNSET:
            field_dict["spans"] = spans
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document import Document
        from ..models.llm_span import LlmSpan
        from ..models.message import Message
        from ..models.retriever_span import RetrieverSpan
        from ..models.step_with_child_spans import StepWithChildSpans
        from ..models.tool_span import ToolSpan
        from ..models.workflow_span_input_type_3 import WorkflowSpanInputType3
        from ..models.workflow_span_input_type_7_item import WorkflowSpanInputType7Item
        from ..models.workflow_span_input_type_8_item import WorkflowSpanInputType8Item
        from ..models.workflow_span_metadata import WorkflowSpanMetadata
        from ..models.workflow_span_output_type_3 import WorkflowSpanOutputType3
        from ..models.workflow_span_output_type_7_item import WorkflowSpanOutputType7Item
        from ..models.workflow_span_output_type_8_item import WorkflowSpanOutputType8Item

        d = src_dict.copy()

        def _parse_input_(
            data: object,
        ) -> Union[
            "Document",
            "Message",
            "WorkflowSpanInputType3",
            list["Document"],
            list["Message"],
            list["WorkflowSpanInputType7Item"],
            list["WorkflowSpanInputType8Item"],
            list[str],
            str,
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_1 = Document.from_dict(data)

                return input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_2 = Message.from_dict(data)

                return input_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_3 = WorkflowSpanInputType3.from_dict(data)

                return input_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_4 = cast(list[str], data)

                return input_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_5 = []
                _input_type_5 = data
                for input_type_5_item_data in _input_type_5:
                    input_type_5_item = Document.from_dict(input_type_5_item_data)

                    input_type_5.append(input_type_5_item)

                return input_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_6 = []
                _input_type_6 = data
                for input_type_6_item_data in _input_type_6:
                    input_type_6_item = Message.from_dict(input_type_6_item_data)

                    input_type_6.append(input_type_6_item)

                return input_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_7 = []
                _input_type_7 = data
                for input_type_7_item_data in _input_type_7:
                    input_type_7_item = WorkflowSpanInputType7Item.from_dict(input_type_7_item_data)

                    input_type_7.append(input_type_7_item)

                return input_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_8 = []
                _input_type_8 = data
                for input_type_8_item_data in _input_type_8:
                    input_type_8_item = WorkflowSpanInputType8Item.from_dict(input_type_8_item_data)

                    input_type_8.append(input_type_8_item)

                return input_type_8
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "Document",
                    "Message",
                    "WorkflowSpanInputType3",
                    list["Document"],
                    list["Message"],
                    list["WorkflowSpanInputType7Item"],
                    list["WorkflowSpanInputType8Item"],
                    list[str],
                    str,
                ],
                data,
            )

        input_ = _parse_input_(d.pop("input"))

        created_at_ns = d.pop("created_at_ns", UNSET)

        duration_ns = d.pop("duration_ns", UNSET)

        def _parse_ground_truth(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, WorkflowSpanMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = WorkflowSpanMetadata.from_dict(_metadata)

        name = d.pop("name", UNSET)

        def _parse_output(
            data: object,
        ) -> Union[
            "Document",
            "Message",
            "WorkflowSpanOutputType3",
            Unset,
            list["Document"],
            list["Message"],
            list["WorkflowSpanOutputType7Item"],
            list["WorkflowSpanOutputType8Item"],
            list[str],
            str,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_1 = Document.from_dict(data)

                return output_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_2 = Message.from_dict(data)

                return output_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_3 = WorkflowSpanOutputType3.from_dict(data)

                return output_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_4 = cast(list[str], data)

                return output_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_5 = []
                _output_type_5 = data
                for output_type_5_item_data in _output_type_5:
                    output_type_5_item = Document.from_dict(output_type_5_item_data)

                    output_type_5.append(output_type_5_item)

                return output_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_6 = []
                _output_type_6 = data
                for output_type_6_item_data in _output_type_6:
                    output_type_6_item = Message.from_dict(output_type_6_item_data)

                    output_type_6.append(output_type_6_item)

                return output_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_7 = []
                _output_type_7 = data
                for output_type_7_item_data in _output_type_7:
                    output_type_7_item = WorkflowSpanOutputType7Item.from_dict(output_type_7_item_data)

                    output_type_7.append(output_type_7_item)

                return output_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_8 = []
                _output_type_8 = data
                for output_type_8_item_data in _output_type_8:
                    output_type_8_item = WorkflowSpanOutputType8Item.from_dict(output_type_8_item_data)

                    output_type_8.append(output_type_8_item)

                return output_type_8
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "Document",
                    "Message",
                    "WorkflowSpanOutputType3",
                    Unset,
                    list["Document"],
                    list["Message"],
                    list["WorkflowSpanOutputType7Item"],
                    list["WorkflowSpanOutputType8Item"],
                    list[str],
                    str,
                ],
                data,
            )

        output = _parse_output(d.pop("output", UNSET))

        def _parse_parent(data: object) -> Union["StepWithChildSpans", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_type_0 = StepWithChildSpans.from_dict(data)

                return parent_type_0
            except:  # noqa: E722
                pass
            return cast(Union["StepWithChildSpans", None, Unset], data)

        parent = _parse_parent(d.pop("parent", UNSET))

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

        type_ = cast(Union[Literal["workflow"], Unset], d.pop("type", UNSET))
        if type_ != "workflow" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'workflow', got '{type_}'")

        workflow_span = cls(
            input_=input_,
            created_at_ns=created_at_ns,
            duration_ns=duration_ns,
            ground_truth=ground_truth,
            metadata=metadata,
            name=name,
            output=output,
            parent=parent,
            spans=spans,
            status_code=status_code,
            type_=type_,
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
