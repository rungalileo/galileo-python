from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.messages_list_item import MessagesListItem
    from ..models.tool_step_input_type_3 import ToolStepInputType3
    from ..models.tool_step_input_type_7_item import ToolStepInputType7Item
    from ..models.tool_step_input_type_8_item import ToolStepInputType8Item
    from ..models.tool_step_metadata import ToolStepMetadata
    from ..models.tool_step_output_type_3 import ToolStepOutputType3
    from ..models.tool_step_output_type_7_item import ToolStepOutputType7Item
    from ..models.tool_step_output_type_8_item import ToolStepOutputType8Item
    from ..models.tool_step_redacted_input_type_3 import ToolStepRedactedInputType3
    from ..models.tool_step_redacted_input_type_7_item import ToolStepRedactedInputType7Item
    from ..models.tool_step_redacted_input_type_8_item import ToolStepRedactedInputType8Item
    from ..models.tool_step_redacted_output_type_3 import ToolStepRedactedOutputType3
    from ..models.tool_step_redacted_output_type_7_item import ToolStepRedactedOutputType7Item
    from ..models.tool_step_redacted_output_type_8_item import ToolStepRedactedOutputType8Item


T = TypeVar("T", bound="ToolStep")


@_attrs_define
class ToolStep:
    """
    Attributes:
        input_ (Document | list[Document] | list[MessagesListItem] | list[str] | list[ToolStepInputType7Item] |
            list[ToolStepInputType8Item] | MessagesListItem | str | ToolStepInputType3): Input to the step.
        type_ (Literal['tool'] | Unset): Type of the step. By default, it is set to tool. Default: 'tool'.
        redacted_input (Document | list[Document] | list[MessagesListItem] | list[str] |
            list[ToolStepRedactedInputType7Item] | list[ToolStepRedactedInputType8Item] | MessagesListItem | None | str |
            ToolStepRedactedInputType3 | Unset): Redacted input of the step. This is used to redact sensitive information.
        output (Document | list[Document] | list[MessagesListItem] | list[str] | list[ToolStepOutputType7Item] |
            list[ToolStepOutputType8Item] | MessagesListItem | str | ToolStepOutputType3 | Unset): Output of the step.
            Default: ''.
        redacted_output (Document | list[Document] | list[MessagesListItem] | list[str] |
            list[ToolStepRedactedOutputType7Item] | list[ToolStepRedactedOutputType8Item] | MessagesListItem | None | str |
            ToolStepRedactedOutputType3 | Unset): Redacted output of the step. This is used to redact sensitive information.
        name (str | Unset): Name of the step. Default: ''.
        created_at_ns (int | Unset): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (int | Unset): Duration of the step in nanoseconds. Default: 0.
        metadata (ToolStepMetadata | Unset): Metadata associated with this step.
        status_code (int | None | Unset): Status code of the step. Used for logging failed/errored steps.
        ground_truth (None | str | Unset): Ground truth expected output for the step.
    """

    input_: (
        Document
        | list[Document]
        | list[MessagesListItem]
        | list[str]
        | list[ToolStepInputType7Item]
        | list[ToolStepInputType8Item]
        | MessagesListItem
        | str
        | ToolStepInputType3
    )
    type_: Literal["tool"] | Unset = "tool"
    redacted_input: (
        Document
        | list[Document]
        | list[MessagesListItem]
        | list[str]
        | list[ToolStepRedactedInputType7Item]
        | list[ToolStepRedactedInputType8Item]
        | MessagesListItem
        | None
        | str
        | ToolStepRedactedInputType3
        | Unset
    ) = UNSET
    output: (
        Document
        | list[Document]
        | list[MessagesListItem]
        | list[str]
        | list[ToolStepOutputType7Item]
        | list[ToolStepOutputType8Item]
        | MessagesListItem
        | str
        | ToolStepOutputType3
        | Unset
    ) = ""
    redacted_output: (
        Document
        | list[Document]
        | list[MessagesListItem]
        | list[str]
        | list[ToolStepRedactedOutputType7Item]
        | list[ToolStepRedactedOutputType8Item]
        | MessagesListItem
        | None
        | str
        | ToolStepRedactedOutputType3
        | Unset
    ) = UNSET
    name: str | Unset = ""
    created_at_ns: int | Unset = UNSET
    duration_ns: int | Unset = 0
    metadata: ToolStepMetadata | Unset = UNSET
    status_code: int | None | Unset = UNSET
    ground_truth: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.document import Document
        from ..models.messages_list_item import MessagesListItem
        from ..models.tool_step_input_type_3 import ToolStepInputType3
        from ..models.tool_step_output_type_3 import ToolStepOutputType3
        from ..models.tool_step_redacted_input_type_3 import ToolStepRedactedInputType3
        from ..models.tool_step_redacted_output_type_3 import ToolStepRedactedOutputType3

        input_: dict[str, Any] | list[dict[str, Any]] | list[str] | str
        if isinstance(self.input_, Document):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, MessagesListItem):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, ToolStepInputType3):
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

        type_ = self.type_

        redacted_input: dict[str, Any] | list[dict[str, Any]] | list[str] | None | str | Unset
        if isinstance(self.redacted_input, Unset):
            redacted_input = UNSET
        elif isinstance(self.redacted_input, Document):
            redacted_input = self.redacted_input.to_dict()
        elif isinstance(self.redacted_input, MessagesListItem):
            redacted_input = self.redacted_input.to_dict()
        elif isinstance(self.redacted_input, ToolStepRedactedInputType3):
            redacted_input = self.redacted_input.to_dict()
        elif isinstance(self.redacted_input, list):
            redacted_input = self.redacted_input

        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_5_item_data in self.redacted_input:
                redacted_input_type_5_item = redacted_input_type_5_item_data.to_dict()
                redacted_input.append(redacted_input_type_5_item)

        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_6_item_data in self.redacted_input:
                redacted_input_type_6_item = redacted_input_type_6_item_data.to_dict()
                redacted_input.append(redacted_input_type_6_item)

        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_7_item_data in self.redacted_input:
                redacted_input_type_7_item = redacted_input_type_7_item_data.to_dict()
                redacted_input.append(redacted_input_type_7_item)

        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_8_item_data in self.redacted_input:
                redacted_input_type_8_item = redacted_input_type_8_item_data.to_dict()
                redacted_input.append(redacted_input_type_8_item)

        else:
            redacted_input = self.redacted_input

        output: dict[str, Any] | list[dict[str, Any]] | list[str] | str | Unset
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, Document):
            output = self.output.to_dict()
        elif isinstance(self.output, MessagesListItem):
            output = self.output.to_dict()
        elif isinstance(self.output, ToolStepOutputType3):
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

        redacted_output: dict[str, Any] | list[dict[str, Any]] | list[str] | None | str | Unset
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        elif isinstance(self.redacted_output, Document):
            redacted_output = self.redacted_output.to_dict()
        elif isinstance(self.redacted_output, MessagesListItem):
            redacted_output = self.redacted_output.to_dict()
        elif isinstance(self.redacted_output, ToolStepRedactedOutputType3):
            redacted_output = self.redacted_output.to_dict()
        elif isinstance(self.redacted_output, list):
            redacted_output = self.redacted_output

        elif isinstance(self.redacted_output, list):
            redacted_output = []
            for redacted_output_type_5_item_data in self.redacted_output:
                redacted_output_type_5_item = redacted_output_type_5_item_data.to_dict()
                redacted_output.append(redacted_output_type_5_item)

        elif isinstance(self.redacted_output, list):
            redacted_output = []
            for redacted_output_type_6_item_data in self.redacted_output:
                redacted_output_type_6_item = redacted_output_type_6_item_data.to_dict()
                redacted_output.append(redacted_output_type_6_item)

        elif isinstance(self.redacted_output, list):
            redacted_output = []
            for redacted_output_type_7_item_data in self.redacted_output:
                redacted_output_type_7_item = redacted_output_type_7_item_data.to_dict()
                redacted_output.append(redacted_output_type_7_item)

        elif isinstance(self.redacted_output, list):
            redacted_output = []
            for redacted_output_type_8_item_data in self.redacted_output:
                redacted_output_type_8_item = redacted_output_type_8_item_data.to_dict()
                redacted_output.append(redacted_output_type_8_item)

        else:
            redacted_output = self.redacted_output

        name = self.name

        created_at_ns = self.created_at_ns

        duration_ns = self.duration_ns

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        status_code: int | None | Unset
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        ground_truth: None | str | Unset
        if isinstance(self.ground_truth, Unset):
            ground_truth = UNSET
        else:
            ground_truth = self.ground_truth

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if redacted_input is not UNSET:
            field_dict["redacted_input"] = redacted_input
        if output is not UNSET:
            field_dict["output"] = output
        if redacted_output is not UNSET:
            field_dict["redacted_output"] = redacted_output
        if name is not UNSET:
            field_dict["name"] = name
        if created_at_ns is not UNSET:
            field_dict["created_at_ns"] = created_at_ns
        if duration_ns is not UNSET:
            field_dict["duration_ns"] = duration_ns
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document import Document
        from ..models.messages_list_item import MessagesListItem
        from ..models.tool_step_input_type_3 import ToolStepInputType3
        from ..models.tool_step_input_type_7_item import ToolStepInputType7Item
        from ..models.tool_step_input_type_8_item import ToolStepInputType8Item
        from ..models.tool_step_metadata import ToolStepMetadata
        from ..models.tool_step_output_type_3 import ToolStepOutputType3
        from ..models.tool_step_output_type_7_item import ToolStepOutputType7Item
        from ..models.tool_step_output_type_8_item import ToolStepOutputType8Item
        from ..models.tool_step_redacted_input_type_3 import ToolStepRedactedInputType3
        from ..models.tool_step_redacted_input_type_7_item import ToolStepRedactedInputType7Item
        from ..models.tool_step_redacted_input_type_8_item import ToolStepRedactedInputType8Item
        from ..models.tool_step_redacted_output_type_3 import ToolStepRedactedOutputType3
        from ..models.tool_step_redacted_output_type_7_item import ToolStepRedactedOutputType7Item
        from ..models.tool_step_redacted_output_type_8_item import ToolStepRedactedOutputType8Item

        d = dict(src_dict)

        def _parse_input_(
            data: object,
        ) -> (
            Document
            | list[Document]
            | list[MessagesListItem]
            | list[str]
            | list[ToolStepInputType7Item]
            | list[ToolStepInputType8Item]
            | MessagesListItem
            | str
            | ToolStepInputType3
        ):
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
                input_type_2 = MessagesListItem.from_dict(data)

                return input_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_3 = ToolStepInputType3.from_dict(data)

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
                    input_type_6_item = MessagesListItem.from_dict(input_type_6_item_data)

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
                    input_type_7_item = ToolStepInputType7Item.from_dict(input_type_7_item_data)

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
                    input_type_8_item = ToolStepInputType8Item.from_dict(input_type_8_item_data)

                    input_type_8.append(input_type_8_item)

                return input_type_8
            except:  # noqa: E722
                pass
            return cast(
                Document
                | list[Document]
                | list[MessagesListItem]
                | list[str]
                | list[ToolStepInputType7Item]
                | list[ToolStepInputType8Item]
                | MessagesListItem
                | str
                | ToolStepInputType3,
                data,
            )

        input_ = _parse_input_(d.pop("input"))

        type_ = cast(Literal["tool"] | Unset, d.pop("type", UNSET))
        if type_ != "tool" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'tool', got '{type_}'")

        def _parse_redacted_input(
            data: object,
        ) -> (
            Document
            | list[Document]
            | list[MessagesListItem]
            | list[str]
            | list[ToolStepRedactedInputType7Item]
            | list[ToolStepRedactedInputType8Item]
            | MessagesListItem
            | None
            | str
            | ToolStepRedactedInputType3
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_input_type_1 = Document.from_dict(data)

                return redacted_input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_input_type_2 = MessagesListItem.from_dict(data)

                return redacted_input_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_input_type_3 = ToolStepRedactedInputType3.from_dict(data)

                return redacted_input_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_4 = cast(list[str], data)

                return redacted_input_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_5 = []
                _redacted_input_type_5 = data
                for redacted_input_type_5_item_data in _redacted_input_type_5:
                    redacted_input_type_5_item = Document.from_dict(redacted_input_type_5_item_data)

                    redacted_input_type_5.append(redacted_input_type_5_item)

                return redacted_input_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_6 = []
                _redacted_input_type_6 = data
                for redacted_input_type_6_item_data in _redacted_input_type_6:
                    redacted_input_type_6_item = MessagesListItem.from_dict(redacted_input_type_6_item_data)

                    redacted_input_type_6.append(redacted_input_type_6_item)

                return redacted_input_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_7 = []
                _redacted_input_type_7 = data
                for redacted_input_type_7_item_data in _redacted_input_type_7:
                    redacted_input_type_7_item = ToolStepRedactedInputType7Item.from_dict(
                        redacted_input_type_7_item_data
                    )

                    redacted_input_type_7.append(redacted_input_type_7_item)

                return redacted_input_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_8 = []
                _redacted_input_type_8 = data
                for redacted_input_type_8_item_data in _redacted_input_type_8:
                    redacted_input_type_8_item = ToolStepRedactedInputType8Item.from_dict(
                        redacted_input_type_8_item_data
                    )

                    redacted_input_type_8.append(redacted_input_type_8_item)

                return redacted_input_type_8
            except:  # noqa: E722
                pass
            return cast(
                Document
                | list[Document]
                | list[MessagesListItem]
                | list[str]
                | list[ToolStepRedactedInputType7Item]
                | list[ToolStepRedactedInputType8Item]
                | MessagesListItem
                | None
                | str
                | ToolStepRedactedInputType3
                | Unset,
                data,
            )

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        def _parse_output(
            data: object,
        ) -> (
            Document
            | list[Document]
            | list[MessagesListItem]
            | list[str]
            | list[ToolStepOutputType7Item]
            | list[ToolStepOutputType8Item]
            | MessagesListItem
            | str
            | ToolStepOutputType3
            | Unset
        ):
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
                output_type_2 = MessagesListItem.from_dict(data)

                return output_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_3 = ToolStepOutputType3.from_dict(data)

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
                    output_type_6_item = MessagesListItem.from_dict(output_type_6_item_data)

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
                    output_type_7_item = ToolStepOutputType7Item.from_dict(output_type_7_item_data)

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
                    output_type_8_item = ToolStepOutputType8Item.from_dict(output_type_8_item_data)

                    output_type_8.append(output_type_8_item)

                return output_type_8
            except:  # noqa: E722
                pass
            return cast(
                Document
                | list[Document]
                | list[MessagesListItem]
                | list[str]
                | list[ToolStepOutputType7Item]
                | list[ToolStepOutputType8Item]
                | MessagesListItem
                | str
                | ToolStepOutputType3
                | Unset,
                data,
            )

        output = _parse_output(d.pop("output", UNSET))

        def _parse_redacted_output(
            data: object,
        ) -> (
            Document
            | list[Document]
            | list[MessagesListItem]
            | list[str]
            | list[ToolStepRedactedOutputType7Item]
            | list[ToolStepRedactedOutputType8Item]
            | MessagesListItem
            | None
            | str
            | ToolStepRedactedOutputType3
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_output_type_1 = Document.from_dict(data)

                return redacted_output_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_output_type_2 = MessagesListItem.from_dict(data)

                return redacted_output_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redacted_output_type_3 = ToolStepRedactedOutputType3.from_dict(data)

                return redacted_output_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_4 = cast(list[str], data)

                return redacted_output_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_5 = []
                _redacted_output_type_5 = data
                for redacted_output_type_5_item_data in _redacted_output_type_5:
                    redacted_output_type_5_item = Document.from_dict(redacted_output_type_5_item_data)

                    redacted_output_type_5.append(redacted_output_type_5_item)

                return redacted_output_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_6 = []
                _redacted_output_type_6 = data
                for redacted_output_type_6_item_data in _redacted_output_type_6:
                    redacted_output_type_6_item = MessagesListItem.from_dict(redacted_output_type_6_item_data)

                    redacted_output_type_6.append(redacted_output_type_6_item)

                return redacted_output_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_7 = []
                _redacted_output_type_7 = data
                for redacted_output_type_7_item_data in _redacted_output_type_7:
                    redacted_output_type_7_item = ToolStepRedactedOutputType7Item.from_dict(
                        redacted_output_type_7_item_data
                    )

                    redacted_output_type_7.append(redacted_output_type_7_item)

                return redacted_output_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_8 = []
                _redacted_output_type_8 = data
                for redacted_output_type_8_item_data in _redacted_output_type_8:
                    redacted_output_type_8_item = ToolStepRedactedOutputType8Item.from_dict(
                        redacted_output_type_8_item_data
                    )

                    redacted_output_type_8.append(redacted_output_type_8_item)

                return redacted_output_type_8
            except:  # noqa: E722
                pass
            return cast(
                Document
                | list[Document]
                | list[MessagesListItem]
                | list[str]
                | list[ToolStepRedactedOutputType7Item]
                | list[ToolStepRedactedOutputType8Item]
                | MessagesListItem
                | None
                | str
                | ToolStepRedactedOutputType3
                | Unset,
                data,
            )

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        created_at_ns = d.pop("created_at_ns", UNSET)

        duration_ns = d.pop("duration_ns", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ToolStepMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ToolStepMetadata.from_dict(_metadata)

        def _parse_status_code(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        def _parse_ground_truth(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        tool_step = cls(
            input_=input_,
            type_=type_,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at_ns=created_at_ns,
            duration_ns=duration_ns,
            metadata=metadata,
            status_code=status_code,
            ground_truth=ground_truth,
        )

        tool_step.additional_properties = d
        return tool_step

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
