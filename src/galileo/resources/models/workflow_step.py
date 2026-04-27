from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_step import AgentStep
    from ..models.chain_step import ChainStep
    from ..models.document import Document
    from ..models.llm_step import LlmStep
    from ..models.messages_list_item import MessagesListItem
    from ..models.retriever_step import RetrieverStep
    from ..models.step_with_children import StepWithChildren
    from ..models.tool_step import ToolStep
    from ..models.workflow_step_input_type_3 import WorkflowStepInputType3
    from ..models.workflow_step_input_type_7_item import WorkflowStepInputType7Item
    from ..models.workflow_step_input_type_8_item import WorkflowStepInputType8Item
    from ..models.workflow_step_metadata import WorkflowStepMetadata
    from ..models.workflow_step_output_type_3 import WorkflowStepOutputType3
    from ..models.workflow_step_output_type_7_item import WorkflowStepOutputType7Item
    from ..models.workflow_step_output_type_8_item import WorkflowStepOutputType8Item
    from ..models.workflow_step_redacted_input_type_3 import WorkflowStepRedactedInputType3
    from ..models.workflow_step_redacted_input_type_7_item import WorkflowStepRedactedInputType7Item
    from ..models.workflow_step_redacted_input_type_8_item import WorkflowStepRedactedInputType8Item
    from ..models.workflow_step_redacted_output_type_3 import WorkflowStepRedactedOutputType3
    from ..models.workflow_step_redacted_output_type_7_item import WorkflowStepRedactedOutputType7Item
    from ..models.workflow_step_redacted_output_type_8_item import WorkflowStepRedactedOutputType8Item


T = TypeVar("T", bound="WorkflowStep")


@_attrs_define
class WorkflowStep:
    """
    Attributes:
        input_ (Document | list[Document] | list[MessagesListItem] | list[str] | list[WorkflowStepInputType7Item] |
            list[WorkflowStepInputType8Item] | MessagesListItem | str | WorkflowStepInputType3): Input to the step.
        type_ (Literal['workflow'] | Unset): Type of the step. By default, it is set to workflow. Default: 'workflow'.
        redacted_input (Document | list[Document] | list[MessagesListItem] | list[str] |
            list[WorkflowStepRedactedInputType7Item] | list[WorkflowStepRedactedInputType8Item] | MessagesListItem | None |
            str | Unset | WorkflowStepRedactedInputType3): Redacted input of the step. This is used to redact sensitive
            information.
        output (Document | list[Document] | list[MessagesListItem] | list[str] | list[WorkflowStepOutputType7Item] |
            list[WorkflowStepOutputType8Item] | MessagesListItem | str | Unset | WorkflowStepOutputType3): Output of the
            step. Default: ''.
        redacted_output (Document | list[Document] | list[MessagesListItem] | list[str] |
            list[WorkflowStepRedactedOutputType7Item] | list[WorkflowStepRedactedOutputType8Item] | MessagesListItem | None
            | str | Unset | WorkflowStepRedactedOutputType3): Redacted output of the step. This is used to redact sensitive
            information.
        name (str | Unset): Name of the step. Default: ''.
        created_at_ns (int | Unset): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (int | Unset): Duration of the step in nanoseconds. Default: 0.
        metadata (WorkflowStepMetadata | Unset): Metadata associated with this step.
        status_code (int | None | Unset): Status code of the step. Used for logging failed/errored steps.
        ground_truth (None | str | Unset): Ground truth expected output for the step.
        steps (list[AgentStep | ChainStep | LlmStep | RetrieverStep | ToolStep | WorkflowStep] | Unset): Steps in the
            workflow.
        parent (None | StepWithChildren | Unset): Parent node of the current node. For internal use only.
    """

    input_: (
        Document
        | list[Document]
        | list[MessagesListItem]
        | list[str]
        | list[WorkflowStepInputType7Item]
        | list[WorkflowStepInputType8Item]
        | MessagesListItem
        | str
        | WorkflowStepInputType3
    )
    type_: Literal["workflow"] | Unset = "workflow"
    redacted_input: (
        Document
        | list[Document]
        | list[MessagesListItem]
        | list[str]
        | list[WorkflowStepRedactedInputType7Item]
        | list[WorkflowStepRedactedInputType8Item]
        | MessagesListItem
        | None
        | str
        | Unset
        | WorkflowStepRedactedInputType3
    ) = UNSET
    output: (
        Document
        | list[Document]
        | list[MessagesListItem]
        | list[str]
        | list[WorkflowStepOutputType7Item]
        | list[WorkflowStepOutputType8Item]
        | MessagesListItem
        | str
        | Unset
        | WorkflowStepOutputType3
    ) = ""
    redacted_output: (
        Document
        | list[Document]
        | list[MessagesListItem]
        | list[str]
        | list[WorkflowStepRedactedOutputType7Item]
        | list[WorkflowStepRedactedOutputType8Item]
        | MessagesListItem
        | None
        | str
        | Unset
        | WorkflowStepRedactedOutputType3
    ) = UNSET
    name: str | Unset = ""
    created_at_ns: int | Unset = UNSET
    duration_ns: int | Unset = 0
    metadata: WorkflowStepMetadata | Unset = UNSET
    status_code: int | None | Unset = UNSET
    ground_truth: None | str | Unset = UNSET
    steps: list[AgentStep | ChainStep | LlmStep | RetrieverStep | ToolStep | WorkflowStep] | Unset = UNSET
    parent: None | StepWithChildren | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_step import ChainStep
        from ..models.document import Document
        from ..models.llm_step import LlmStep
        from ..models.messages_list_item import MessagesListItem
        from ..models.retriever_step import RetrieverStep
        from ..models.step_with_children import StepWithChildren
        from ..models.tool_step import ToolStep
        from ..models.workflow_step_input_type_3 import WorkflowStepInputType3
        from ..models.workflow_step_output_type_3 import WorkflowStepOutputType3
        from ..models.workflow_step_redacted_input_type_3 import WorkflowStepRedactedInputType3
        from ..models.workflow_step_redacted_output_type_3 import WorkflowStepRedactedOutputType3

        input_: dict[str, Any] | list[dict[str, Any]] | list[str] | str
        if isinstance(self.input_, Document):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, MessagesListItem):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, WorkflowStepInputType3):
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
        elif isinstance(self.redacted_input, WorkflowStepRedactedInputType3):
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
        elif isinstance(self.output, WorkflowStepOutputType3):
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
        elif isinstance(self.redacted_output, WorkflowStepRedactedOutputType3):
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

        steps: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for steps_item_data in self.steps:
                steps_item: dict[str, Any]
                if isinstance(steps_item_data, WorkflowStep):
                    steps_item = steps_item_data.to_dict()
                elif isinstance(steps_item_data, ChainStep):
                    steps_item = steps_item_data.to_dict()
                elif isinstance(steps_item_data, LlmStep):
                    steps_item = steps_item_data.to_dict()
                elif isinstance(steps_item_data, RetrieverStep):
                    steps_item = steps_item_data.to_dict()
                elif isinstance(steps_item_data, ToolStep):
                    steps_item = steps_item_data.to_dict()
                else:
                    steps_item = steps_item_data.to_dict()

                steps.append(steps_item)

        parent: dict[str, Any] | None | Unset
        if isinstance(self.parent, Unset):
            parent = UNSET
        elif isinstance(self.parent, StepWithChildren):
            parent = self.parent.to_dict()
        else:
            parent = self.parent

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
        if steps is not UNSET:
            field_dict["steps"] = steps
        if parent is not UNSET:
            field_dict["parent"] = parent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_step import AgentStep
        from ..models.chain_step import ChainStep
        from ..models.document import Document
        from ..models.llm_step import LlmStep
        from ..models.messages_list_item import MessagesListItem
        from ..models.retriever_step import RetrieverStep
        from ..models.step_with_children import StepWithChildren
        from ..models.tool_step import ToolStep
        from ..models.workflow_step_input_type_3 import WorkflowStepInputType3
        from ..models.workflow_step_input_type_7_item import WorkflowStepInputType7Item
        from ..models.workflow_step_input_type_8_item import WorkflowStepInputType8Item
        from ..models.workflow_step_metadata import WorkflowStepMetadata
        from ..models.workflow_step_output_type_3 import WorkflowStepOutputType3
        from ..models.workflow_step_output_type_7_item import WorkflowStepOutputType7Item
        from ..models.workflow_step_output_type_8_item import WorkflowStepOutputType8Item
        from ..models.workflow_step_redacted_input_type_3 import WorkflowStepRedactedInputType3
        from ..models.workflow_step_redacted_input_type_7_item import WorkflowStepRedactedInputType7Item
        from ..models.workflow_step_redacted_input_type_8_item import WorkflowStepRedactedInputType8Item
        from ..models.workflow_step_redacted_output_type_3 import WorkflowStepRedactedOutputType3
        from ..models.workflow_step_redacted_output_type_7_item import WorkflowStepRedactedOutputType7Item
        from ..models.workflow_step_redacted_output_type_8_item import WorkflowStepRedactedOutputType8Item

        d = dict(src_dict)

        def _parse_input_(
            data: object,
        ) -> (
            Document
            | list[Document]
            | list[MessagesListItem]
            | list[str]
            | list[WorkflowStepInputType7Item]
            | list[WorkflowStepInputType8Item]
            | MessagesListItem
            | str
            | WorkflowStepInputType3
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
                input_type_3 = WorkflowStepInputType3.from_dict(data)

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
                    input_type_7_item = WorkflowStepInputType7Item.from_dict(input_type_7_item_data)

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
                    input_type_8_item = WorkflowStepInputType8Item.from_dict(input_type_8_item_data)

                    input_type_8.append(input_type_8_item)

                return input_type_8
            except:  # noqa: E722
                pass
            return cast(
                Document
                | list[Document]
                | list[MessagesListItem]
                | list[str]
                | list[WorkflowStepInputType7Item]
                | list[WorkflowStepInputType8Item]
                | MessagesListItem
                | str
                | WorkflowStepInputType3,
                data,
            )

        input_ = _parse_input_(d.pop("input"))

        type_ = cast(Literal["workflow"] | Unset, d.pop("type", UNSET))
        if type_ != "workflow" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'workflow', got '{type_}'")

        def _parse_redacted_input(
            data: object,
        ) -> (
            Document
            | list[Document]
            | list[MessagesListItem]
            | list[str]
            | list[WorkflowStepRedactedInputType7Item]
            | list[WorkflowStepRedactedInputType8Item]
            | MessagesListItem
            | None
            | str
            | Unset
            | WorkflowStepRedactedInputType3
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
                redacted_input_type_3 = WorkflowStepRedactedInputType3.from_dict(data)

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
                    redacted_input_type_7_item = WorkflowStepRedactedInputType7Item.from_dict(
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
                    redacted_input_type_8_item = WorkflowStepRedactedInputType8Item.from_dict(
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
                | list[WorkflowStepRedactedInputType7Item]
                | list[WorkflowStepRedactedInputType8Item]
                | MessagesListItem
                | None
                | str
                | Unset
                | WorkflowStepRedactedInputType3,
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
            | list[WorkflowStepOutputType7Item]
            | list[WorkflowStepOutputType8Item]
            | MessagesListItem
            | str
            | Unset
            | WorkflowStepOutputType3
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
                output_type_3 = WorkflowStepOutputType3.from_dict(data)

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
                    output_type_7_item = WorkflowStepOutputType7Item.from_dict(output_type_7_item_data)

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
                    output_type_8_item = WorkflowStepOutputType8Item.from_dict(output_type_8_item_data)

                    output_type_8.append(output_type_8_item)

                return output_type_8
            except:  # noqa: E722
                pass
            return cast(
                Document
                | list[Document]
                | list[MessagesListItem]
                | list[str]
                | list[WorkflowStepOutputType7Item]
                | list[WorkflowStepOutputType8Item]
                | MessagesListItem
                | str
                | Unset
                | WorkflowStepOutputType3,
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
            | list[WorkflowStepRedactedOutputType7Item]
            | list[WorkflowStepRedactedOutputType8Item]
            | MessagesListItem
            | None
            | str
            | Unset
            | WorkflowStepRedactedOutputType3
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
                redacted_output_type_3 = WorkflowStepRedactedOutputType3.from_dict(data)

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
                    redacted_output_type_7_item = WorkflowStepRedactedOutputType7Item.from_dict(
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
                    redacted_output_type_8_item = WorkflowStepRedactedOutputType8Item.from_dict(
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
                | list[WorkflowStepRedactedOutputType7Item]
                | list[WorkflowStepRedactedOutputType8Item]
                | MessagesListItem
                | None
                | str
                | Unset
                | WorkflowStepRedactedOutputType3,
                data,
            )

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        created_at_ns = d.pop("created_at_ns", UNSET)

        duration_ns = d.pop("duration_ns", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: WorkflowStepMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = WorkflowStepMetadata.from_dict(_metadata)

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

        _steps = d.pop("steps", UNSET)
        steps: list[AgentStep | ChainStep | LlmStep | RetrieverStep | ToolStep | WorkflowStep] | Unset = UNSET
        if _steps is not UNSET:
            steps = []
            for steps_item_data in _steps:

                def _parse_steps_item(
                    data: object,
                ) -> AgentStep | ChainStep | LlmStep | RetrieverStep | ToolStep | WorkflowStep:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        steps_item_type_0 = WorkflowStep.from_dict(data)

                        return steps_item_type_0
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        steps_item_type_1 = ChainStep.from_dict(data)

                        return steps_item_type_1
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        steps_item_type_2 = LlmStep.from_dict(data)

                        return steps_item_type_2
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        steps_item_type_3 = RetrieverStep.from_dict(data)

                        return steps_item_type_3
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        steps_item_type_4 = ToolStep.from_dict(data)

                        return steps_item_type_4
                    except:  # noqa: E722
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    steps_item_type_5 = AgentStep.from_dict(data)

                    return steps_item_type_5

                steps_item = _parse_steps_item(steps_item_data)

                steps.append(steps_item)

        def _parse_parent(data: object) -> None | StepWithChildren | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_type_0 = StepWithChildren.from_dict(data)

                return parent_type_0
            except:  # noqa: E722
                pass
            return cast(None | StepWithChildren | Unset, data)

        parent = _parse_parent(d.pop("parent", UNSET))

        workflow_step = cls(
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
            steps=steps,
            parent=parent,
        )

        workflow_step.additional_properties = d
        return workflow_step

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
