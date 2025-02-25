from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.message import Message
    from ..models.step_with_child_spans import StepWithChildSpans
    from ..models.tool_span_input_type_3 import ToolSpanInputType3
    from ..models.tool_span_input_type_7_item import ToolSpanInputType7Item
    from ..models.tool_span_input_type_8_item import ToolSpanInputType8Item
    from ..models.tool_span_metadata import ToolSpanMetadata
    from ..models.tool_span_output_type_3 import ToolSpanOutputType3
    from ..models.tool_span_output_type_7_item import ToolSpanOutputType7Item
    from ..models.tool_span_output_type_8_item import ToolSpanOutputType8Item


T = TypeVar("T", bound="ToolSpan")


@_attrs_define
class ToolSpan:
    """
    Attributes:
        input_ (Union['Document', 'Message', 'ToolSpanInputType3', list['Document'], list['Message'],
            list['ToolSpanInputType7Item'], list['ToolSpanInputType8Item'], list[str], str]): Input to the step.
        created_at_ns (Union[Unset, int]): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (Union[Unset, int]): Duration of the step in nanoseconds. Default: 0.
        ground_truth (Union[None, Unset, str]): Ground truth expected output for the step.
        metadata (Union[Unset, ToolSpanMetadata]): Metadata associated with this step.
        name (Union[Unset, str]): Name of the step. Default: ''.
        output (Union['Document', 'Message', 'ToolSpanOutputType3', Unset, list['Document'], list['Message'],
            list['ToolSpanOutputType7Item'], list['ToolSpanOutputType8Item'], list[str], str]): Output of the step. Default:
            ''.
        parent (Union['StepWithChildSpans', None, Unset]): Parent node of the current node. For internal use only.
        status_code (Union[None, Unset, int]): Status code of the step. Used for logging failed/errored steps.
        type_ (Union[Literal['tool'], Unset]): Type of the step. By default, it is set to tool. Default: 'tool'.
    """

    input_: Union[
        "Document",
        "Message",
        "ToolSpanInputType3",
        list["Document"],
        list["Message"],
        list["ToolSpanInputType7Item"],
        list["ToolSpanInputType8Item"],
        list[str],
        str,
    ]
    created_at_ns: Union[Unset, int] = UNSET
    duration_ns: Union[Unset, int] = 0
    ground_truth: Union[None, Unset, str] = UNSET
    metadata: Union[Unset, "ToolSpanMetadata"] = UNSET
    name: Union[Unset, str] = ""
    output: Union[
        "Document",
        "Message",
        "ToolSpanOutputType3",
        Unset,
        list["Document"],
        list["Message"],
        list["ToolSpanOutputType7Item"],
        list["ToolSpanOutputType8Item"],
        list[str],
        str,
    ] = ""
    parent: Union["StepWithChildSpans", None, Unset] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    type_: Union[Literal["tool"], Unset] = "tool"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.document import Document
        from ..models.message import Message
        from ..models.step_with_child_spans import StepWithChildSpans
        from ..models.tool_span_input_type_3 import ToolSpanInputType3
        from ..models.tool_span_output_type_3 import ToolSpanOutputType3

        input_: Union[dict[str, Any], list[dict[str, Any]], list[str], str]
        if isinstance(self.input_, Document):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, Message):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, ToolSpanInputType3):
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
        elif isinstance(self.output, ToolSpanOutputType3):
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
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document import Document
        from ..models.message import Message
        from ..models.step_with_child_spans import StepWithChildSpans
        from ..models.tool_span_input_type_3 import ToolSpanInputType3
        from ..models.tool_span_input_type_7_item import ToolSpanInputType7Item
        from ..models.tool_span_input_type_8_item import ToolSpanInputType8Item
        from ..models.tool_span_metadata import ToolSpanMetadata
        from ..models.tool_span_output_type_3 import ToolSpanOutputType3
        from ..models.tool_span_output_type_7_item import ToolSpanOutputType7Item
        from ..models.tool_span_output_type_8_item import ToolSpanOutputType8Item

        d = src_dict.copy()

        def _parse_input_(
            data: object,
        ) -> Union[
            "Document",
            "Message",
            "ToolSpanInputType3",
            list["Document"],
            list["Message"],
            list["ToolSpanInputType7Item"],
            list["ToolSpanInputType8Item"],
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
                input_type_3 = ToolSpanInputType3.from_dict(data)

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
                    input_type_7_item = ToolSpanInputType7Item.from_dict(input_type_7_item_data)

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
                    input_type_8_item = ToolSpanInputType8Item.from_dict(input_type_8_item_data)

                    input_type_8.append(input_type_8_item)

                return input_type_8
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "Document",
                    "Message",
                    "ToolSpanInputType3",
                    list["Document"],
                    list["Message"],
                    list["ToolSpanInputType7Item"],
                    list["ToolSpanInputType8Item"],
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
        metadata: Union[Unset, ToolSpanMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ToolSpanMetadata.from_dict(_metadata)

        name = d.pop("name", UNSET)

        def _parse_output(
            data: object,
        ) -> Union[
            "Document",
            "Message",
            "ToolSpanOutputType3",
            Unset,
            list["Document"],
            list["Message"],
            list["ToolSpanOutputType7Item"],
            list["ToolSpanOutputType8Item"],
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
                output_type_3 = ToolSpanOutputType3.from_dict(data)

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
                    output_type_7_item = ToolSpanOutputType7Item.from_dict(output_type_7_item_data)

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
                    output_type_8_item = ToolSpanOutputType8Item.from_dict(output_type_8_item_data)

                    output_type_8.append(output_type_8_item)

                return output_type_8
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "Document",
                    "Message",
                    "ToolSpanOutputType3",
                    Unset,
                    list["Document"],
                    list["Message"],
                    list["ToolSpanOutputType7Item"],
                    list["ToolSpanOutputType8Item"],
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

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        type_ = cast(Union[Literal["tool"], Unset], d.pop("type", UNSET))
        if type_ != "tool" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'tool', got '{type_}'")

        tool_span = cls(
            input_=input_,
            created_at_ns=created_at_ns,
            duration_ns=duration_ns,
            ground_truth=ground_truth,
            metadata=metadata,
            name=name,
            output=output,
            parent=parent,
            status_code=status_code,
            type_=type_,
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
