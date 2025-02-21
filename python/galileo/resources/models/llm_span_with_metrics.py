from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.llm_span_with_metrics_input_type_3 import LlmSpanWithMetricsInputType3
    from ..models.llm_span_with_metrics_input_type_7_item import LlmSpanWithMetricsInputType7Item
    from ..models.llm_span_with_metrics_input_type_8_item import LlmSpanWithMetricsInputType8Item
    from ..models.llm_span_with_metrics_metadata import LlmSpanWithMetricsMetadata
    from ..models.llm_span_with_metrics_metrics import LlmSpanWithMetricsMetrics
    from ..models.llm_span_with_metrics_output_type_3 import LlmSpanWithMetricsOutputType3
    from ..models.llm_span_with_metrics_output_type_7_item import LlmSpanWithMetricsOutputType7Item
    from ..models.llm_span_with_metrics_output_type_8_item import LlmSpanWithMetricsOutputType8Item
    from ..models.llm_span_with_metrics_tools_type_0_item import LlmSpanWithMetricsToolsType0Item
    from ..models.message import Message
    from ..models.step_with_child_spans import StepWithChildSpans


T = TypeVar("T", bound="LlmSpanWithMetrics")


@_attrs_define
class LlmSpanWithMetrics:
    """
    Attributes:
        input_ (Union['Document', 'LlmSpanWithMetricsInputType3', 'Message', list['Document'],
            list['LlmSpanWithMetricsInputType7Item'], list['LlmSpanWithMetricsInputType8Item'], list['Message'], list[str],
            str]): Input to the step.
        step_id (str):
        trace_id (str):
        created_at_ns (Union[Unset, int]): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (Union[Unset, int]): Duration of the step in nanoseconds. Default: 0.
        ground_truth (Union[None, Unset, str]): Ground truth expected output for the step.
        input_tokens (Union[None, Unset, int]): Number of input tokens.
        metadata (Union[Unset, LlmSpanWithMetricsMetadata]): Metadata associated with this step.
        metrics (Union[Unset, LlmSpanWithMetricsMetrics]):
        model (Union[None, Unset, str]): Model used for this step.
        name (Union[Unset, str]): Name of the step. Default: ''.
        output (Union['Document', 'LlmSpanWithMetricsOutputType3', 'Message', Unset, list['Document'],
            list['LlmSpanWithMetricsOutputType7Item'], list['LlmSpanWithMetricsOutputType8Item'], list['Message'],
            list[str], str]): Output of the step. Default: ''.
        output_tokens (Union[None, Unset, int]): Number of output tokens.
        parent (Union['StepWithChildSpans', None, Unset]): Parent node of the current node. For internal use only.
        parent_id (Union[None, UUID, Unset]):
        status_code (Union[None, Unset, int]): Status code of the step. Used for logging failed/errored steps.
        temperature (Union[None, Unset, float]): Temperature used for generation.
        tools (Union[None, Unset, list['LlmSpanWithMetricsToolsType0Item']]): List of available tools passed to the LLM
            on invocation.
        total_tokens (Union[None, Unset, int]): Total number of tokens.
        type_ (Union[Literal['llm'], Unset]): Type of the step. By default, it is set to llm. Default: 'llm'.
    """

    input_: Union[
        "Document",
        "LlmSpanWithMetricsInputType3",
        "Message",
        list["Document"],
        list["LlmSpanWithMetricsInputType7Item"],
        list["LlmSpanWithMetricsInputType8Item"],
        list["Message"],
        list[str],
        str,
    ]
    step_id: str
    trace_id: str
    created_at_ns: Union[Unset, int] = UNSET
    duration_ns: Union[Unset, int] = 0
    ground_truth: Union[None, Unset, str] = UNSET
    input_tokens: Union[None, Unset, int] = UNSET
    metadata: Union[Unset, "LlmSpanWithMetricsMetadata"] = UNSET
    metrics: Union[Unset, "LlmSpanWithMetricsMetrics"] = UNSET
    model: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = ""
    output: Union[
        "Document",
        "LlmSpanWithMetricsOutputType3",
        "Message",
        Unset,
        list["Document"],
        list["LlmSpanWithMetricsOutputType7Item"],
        list["LlmSpanWithMetricsOutputType8Item"],
        list["Message"],
        list[str],
        str,
    ] = ""
    output_tokens: Union[None, Unset, int] = UNSET
    parent: Union["StepWithChildSpans", None, Unset] = UNSET
    parent_id: Union[None, UUID, Unset] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    temperature: Union[None, Unset, float] = UNSET
    tools: Union[None, Unset, list["LlmSpanWithMetricsToolsType0Item"]] = UNSET
    total_tokens: Union[None, Unset, int] = UNSET
    type_: Union[Literal["llm"], Unset] = "llm"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.document import Document
        from ..models.llm_span_with_metrics_input_type_3 import LlmSpanWithMetricsInputType3
        from ..models.llm_span_with_metrics_output_type_3 import LlmSpanWithMetricsOutputType3
        from ..models.message import Message
        from ..models.step_with_child_spans import StepWithChildSpans

        input_: Union[dict[str, Any], list[dict[str, Any]], list[str], str]
        if isinstance(self.input_, Document):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, Message):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, LlmSpanWithMetricsInputType3):
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

        step_id = self.step_id

        trace_id = self.trace_id

        created_at_ns = self.created_at_ns

        duration_ns = self.duration_ns

        ground_truth: Union[None, Unset, str]
        if isinstance(self.ground_truth, Unset):
            ground_truth = UNSET
        else:
            ground_truth = self.ground_truth

        input_tokens: Union[None, Unset, int]
        if isinstance(self.input_tokens, Unset):
            input_tokens = UNSET
        else:
            input_tokens = self.input_tokens

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        name = self.name

        output: Union[Unset, dict[str, Any], list[dict[str, Any]], list[str], str]
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, Document):
            output = self.output.to_dict()
        elif isinstance(self.output, Message):
            output = self.output.to_dict()
        elif isinstance(self.output, LlmSpanWithMetricsOutputType3):
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

        output_tokens: Union[None, Unset, int]
        if isinstance(self.output_tokens, Unset):
            output_tokens = UNSET
        else:
            output_tokens = self.output_tokens

        parent: Union[None, Unset, dict[str, Any]]
        if isinstance(self.parent, Unset):
            parent = UNSET
        elif isinstance(self.parent, StepWithChildSpans):
            parent = self.parent.to_dict()
        else:
            parent = self.parent

        parent_id: Union[None, Unset, str]
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        elif isinstance(self.parent_id, UUID):
            parent_id = str(self.parent_id)
        else:
            parent_id = self.parent_id

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        temperature: Union[None, Unset, float]
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

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

        total_tokens: Union[None, Unset, int]
        if isinstance(self.total_tokens, Unset):
            total_tokens = UNSET
        else:
            total_tokens = self.total_tokens

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_, "step_id": step_id, "trace_id": trace_id})
        if created_at_ns is not UNSET:
            field_dict["created_at_ns"] = created_at_ns
        if duration_ns is not UNSET:
            field_dict["duration_ns"] = duration_ns
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if model is not UNSET:
            field_dict["model"] = model
        if name is not UNSET:
            field_dict["name"] = name
        if output is not UNSET:
            field_dict["output"] = output
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if parent is not UNSET:
            field_dict["parent"] = parent
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if tools is not UNSET:
            field_dict["tools"] = tools
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document import Document
        from ..models.llm_span_with_metrics_input_type_3 import LlmSpanWithMetricsInputType3
        from ..models.llm_span_with_metrics_input_type_7_item import LlmSpanWithMetricsInputType7Item
        from ..models.llm_span_with_metrics_input_type_8_item import LlmSpanWithMetricsInputType8Item
        from ..models.llm_span_with_metrics_metadata import LlmSpanWithMetricsMetadata
        from ..models.llm_span_with_metrics_metrics import LlmSpanWithMetricsMetrics
        from ..models.llm_span_with_metrics_output_type_3 import LlmSpanWithMetricsOutputType3
        from ..models.llm_span_with_metrics_output_type_7_item import LlmSpanWithMetricsOutputType7Item
        from ..models.llm_span_with_metrics_output_type_8_item import LlmSpanWithMetricsOutputType8Item
        from ..models.llm_span_with_metrics_tools_type_0_item import LlmSpanWithMetricsToolsType0Item
        from ..models.message import Message
        from ..models.step_with_child_spans import StepWithChildSpans

        d = src_dict.copy()

        def _parse_input_(
            data: object,
        ) -> Union[
            "Document",
            "LlmSpanWithMetricsInputType3",
            "Message",
            list["Document"],
            list["LlmSpanWithMetricsInputType7Item"],
            list["LlmSpanWithMetricsInputType8Item"],
            list["Message"],
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
                input_type_3 = LlmSpanWithMetricsInputType3.from_dict(data)

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
                    input_type_7_item = LlmSpanWithMetricsInputType7Item.from_dict(input_type_7_item_data)

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
                    input_type_8_item = LlmSpanWithMetricsInputType8Item.from_dict(input_type_8_item_data)

                    input_type_8.append(input_type_8_item)

                return input_type_8
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "Document",
                    "LlmSpanWithMetricsInputType3",
                    "Message",
                    list["Document"],
                    list["LlmSpanWithMetricsInputType7Item"],
                    list["LlmSpanWithMetricsInputType8Item"],
                    list["Message"],
                    list[str],
                    str,
                ],
                data,
            )

        input_ = _parse_input_(d.pop("input"))

        step_id = d.pop("step_id")

        trace_id = d.pop("trace_id")

        created_at_ns = d.pop("created_at_ns", UNSET)

        duration_ns = d.pop("duration_ns", UNSET)

        def _parse_ground_truth(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        def _parse_input_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        input_tokens = _parse_input_tokens(d.pop("input_tokens", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, LlmSpanWithMetricsMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = LlmSpanWithMetricsMetadata.from_dict(_metadata)

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, LlmSpanWithMetricsMetrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = LlmSpanWithMetricsMetrics.from_dict(_metrics)

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        name = d.pop("name", UNSET)

        def _parse_output(
            data: object,
        ) -> Union[
            "Document",
            "LlmSpanWithMetricsOutputType3",
            "Message",
            Unset,
            list["Document"],
            list["LlmSpanWithMetricsOutputType7Item"],
            list["LlmSpanWithMetricsOutputType8Item"],
            list["Message"],
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
                output_type_3 = LlmSpanWithMetricsOutputType3.from_dict(data)

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
                    output_type_7_item = LlmSpanWithMetricsOutputType7Item.from_dict(output_type_7_item_data)

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
                    output_type_8_item = LlmSpanWithMetricsOutputType8Item.from_dict(output_type_8_item_data)

                    output_type_8.append(output_type_8_item)

                return output_type_8
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "Document",
                    "LlmSpanWithMetricsOutputType3",
                    "Message",
                    Unset,
                    list["Document"],
                    list["LlmSpanWithMetricsOutputType7Item"],
                    list["LlmSpanWithMetricsOutputType8Item"],
                    list["Message"],
                    list[str],
                    str,
                ],
                data,
            )

        output = _parse_output(d.pop("output", UNSET))

        def _parse_output_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        output_tokens = _parse_output_tokens(d.pop("output_tokens", UNSET))

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

        def _parse_parent_id(data: object) -> Union[None, UUID, Unset]:
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
            return cast(Union[None, UUID, Unset], data)

        parent_id = _parse_parent_id(d.pop("parent_id", UNSET))

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_tools(data: object) -> Union[None, Unset, list["LlmSpanWithMetricsToolsType0Item"]]:
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
                    tools_type_0_item = LlmSpanWithMetricsToolsType0Item.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["LlmSpanWithMetricsToolsType0Item"]], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_total_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_tokens = _parse_total_tokens(d.pop("total_tokens", UNSET))

        type_ = cast(Union[Literal["llm"], Unset], d.pop("type", UNSET))
        if type_ != "llm" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'llm', got '{type_}'")

        llm_span_with_metrics = cls(
            input_=input_,
            step_id=step_id,
            trace_id=trace_id,
            created_at_ns=created_at_ns,
            duration_ns=duration_ns,
            ground_truth=ground_truth,
            input_tokens=input_tokens,
            metadata=metadata,
            metrics=metrics,
            model=model,
            name=name,
            output=output,
            output_tokens=output_tokens,
            parent=parent,
            parent_id=parent_id,
            status_code=status_code,
            temperature=temperature,
            tools=tools,
            total_tokens=total_tokens,
            type_=type_,
        )

        llm_span_with_metrics.additional_properties = d
        return llm_span_with_metrics

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
