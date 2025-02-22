from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_step import AgentStep
    from ..models.chain_step import ChainStep
    from ..models.document import Document
    from ..models.llm_step import LlmStep
    from ..models.message import Message
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


T = TypeVar("T", bound="WorkflowStep")


@_attrs_define
class WorkflowStep:
    """
    Attributes:
        input_ (Union['Document', 'Message', 'WorkflowStepInputType3', list['Document'], list['Message'],
            list['WorkflowStepInputType7Item'], list['WorkflowStepInputType8Item'], list[str], str]): Input to the step.
        created_at_ns (Union[Unset, int]): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (Union[Unset, int]): Duration of the step in nanoseconds. Default: 0.
        ground_truth (Union[None, Unset, str]): Ground truth expected output for the step.
        metadata (Union[Unset, WorkflowStepMetadata]): Metadata associated with this step.
        name (Union[Unset, str]): Name of the step. Default: ''.
        output (Union['Document', 'Message', 'WorkflowStepOutputType3', Unset, list['Document'], list['Message'],
            list['WorkflowStepOutputType7Item'], list['WorkflowStepOutputType8Item'], list[str], str]): Output of the step.
            Default: ''.
        parent (Union['StepWithChildren', None, Unset]): Parent node of the current node. For internal use only.
        status_code (Union[None, Unset, int]): Status code of the step. Used for logging failed/errored steps.
        steps (Union[Unset, list[Union['AgentStep', 'ChainStep', 'LlmStep', 'RetrieverStep', 'ToolStep',
            'WorkflowStep']]]): Steps in the workflow.
        type_ (Union[Literal['workflow'], Unset]): Type of the step. By default, it is set to workflow. Default:
            'workflow'.
    """

    input_: Union[
        "Document",
        "Message",
        "WorkflowStepInputType3",
        list["Document"],
        list["Message"],
        list["WorkflowStepInputType7Item"],
        list["WorkflowStepInputType8Item"],
        list[str],
        str,
    ]
    created_at_ns: Union[Unset, int] = UNSET
    duration_ns: Union[Unset, int] = 0
    ground_truth: Union[None, Unset, str] = UNSET
    metadata: Union[Unset, "WorkflowStepMetadata"] = UNSET
    name: Union[Unset, str] = ""
    output: Union[
        "Document",
        "Message",
        "WorkflowStepOutputType3",
        Unset,
        list["Document"],
        list["Message"],
        list["WorkflowStepOutputType7Item"],
        list["WorkflowStepOutputType8Item"],
        list[str],
        str,
    ] = ""
    parent: Union["StepWithChildren", None, Unset] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    steps: Union[
        Unset, list[Union["AgentStep", "ChainStep", "LlmStep", "RetrieverStep", "ToolStep", "WorkflowStep"]]
    ] = UNSET
    type_: Union[Literal["workflow"], Unset] = "workflow"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_step import ChainStep
        from ..models.document import Document
        from ..models.llm_step import LlmStep
        from ..models.message import Message
        from ..models.retriever_step import RetrieverStep
        from ..models.step_with_children import StepWithChildren
        from ..models.tool_step import ToolStep
        from ..models.workflow_step_input_type_3 import WorkflowStepInputType3
        from ..models.workflow_step_output_type_3 import WorkflowStepOutputType3

        input_: Union[dict[str, Any], list[dict[str, Any]], list[str], str]
        if isinstance(self.input_, Document):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, Message):
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

        parent: Union[None, Unset, dict[str, Any]]
        if isinstance(self.parent, Unset):
            parent = UNSET
        elif isinstance(self.parent, StepWithChildren):
            parent = self.parent.to_dict()
        else:
            parent = self.parent

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        steps: Union[Unset, list[dict[str, Any]]] = UNSET
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
        if steps is not UNSET:
            field_dict["steps"] = steps
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.agent_step import AgentStep
        from ..models.chain_step import ChainStep
        from ..models.document import Document
        from ..models.llm_step import LlmStep
        from ..models.message import Message
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

        d = src_dict.copy()

        def _parse_input_(
            data: object,
        ) -> Union[
            "Document",
            "Message",
            "WorkflowStepInputType3",
            list["Document"],
            list["Message"],
            list["WorkflowStepInputType7Item"],
            list["WorkflowStepInputType8Item"],
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
                Union[
                    "Document",
                    "Message",
                    "WorkflowStepInputType3",
                    list["Document"],
                    list["Message"],
                    list["WorkflowStepInputType7Item"],
                    list["WorkflowStepInputType8Item"],
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
        metadata: Union[Unset, WorkflowStepMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = WorkflowStepMetadata.from_dict(_metadata)

        name = d.pop("name", UNSET)

        def _parse_output(
            data: object,
        ) -> Union[
            "Document",
            "Message",
            "WorkflowStepOutputType3",
            Unset,
            list["Document"],
            list["Message"],
            list["WorkflowStepOutputType7Item"],
            list["WorkflowStepOutputType8Item"],
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
                Union[
                    "Document",
                    "Message",
                    "WorkflowStepOutputType3",
                    Unset,
                    list["Document"],
                    list["Message"],
                    list["WorkflowStepOutputType7Item"],
                    list["WorkflowStepOutputType8Item"],
                    list[str],
                    str,
                ],
                data,
            )

        output = _parse_output(d.pop("output", UNSET))

        def _parse_parent(data: object) -> Union["StepWithChildren", None, Unset]:
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
            return cast(Union["StepWithChildren", None, Unset], data)

        parent = _parse_parent(d.pop("parent", UNSET))

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        steps = []
        _steps = d.pop("steps", UNSET)
        for steps_item_data in _steps or []:

            def _parse_steps_item(
                data: object,
            ) -> Union["AgentStep", "ChainStep", "LlmStep", "RetrieverStep", "ToolStep", "WorkflowStep"]:
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

        type_ = cast(Union[Literal["workflow"], Unset], d.pop("type", UNSET))
        if type_ != "workflow" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'workflow', got '{type_}'")

        workflow_step = cls(
            input_=input_,
            created_at_ns=created_at_ns,
            duration_ns=duration_ns,
            ground_truth=ground_truth,
            metadata=metadata,
            name=name,
            output=output,
            parent=parent,
            status_code=status_code,
            steps=steps,
            type_=type_,
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
