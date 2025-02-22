from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_galileo_step_input_type_3 import BaseGalileoStepInputType3
    from ..models.base_galileo_step_input_type_7_item import BaseGalileoStepInputType7Item
    from ..models.base_galileo_step_input_type_8_item import BaseGalileoStepInputType8Item
    from ..models.base_galileo_step_metadata import BaseGalileoStepMetadata
    from ..models.base_galileo_step_output_type_3 import BaseGalileoStepOutputType3
    from ..models.base_galileo_step_output_type_7_item import BaseGalileoStepOutputType7Item
    from ..models.base_galileo_step_output_type_8_item import BaseGalileoStepOutputType8Item
    from ..models.document import Document
    from ..models.message import Message
    from ..models.step_metric import StepMetric


T = TypeVar("T", bound="BaseGalileoStep")


@_attrs_define
class BaseGalileoStep:
    """
    Attributes:
        input_ (Union['BaseGalileoStepInputType3', 'Document', 'Message', list['BaseGalileoStepInputType7Item'],
            list['BaseGalileoStepInputType8Item'], list['Document'], list['Message'], list[str], str]): Input to the step.
        created_at_ns (Union[Unset, int]): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (Union[Unset, int]): Duration of the step in nanoseconds. Default: 0.
        ground_truth (Union[None, Unset, str]): Ground truth expected output for the step.
        metadata (Union[Unset, BaseGalileoStepMetadata]): Metadata associated with this step.
        metrics (Union[None, Unset, list['StepMetric']]):
        name (Union[Unset, str]): Name of the step. Default: ''.
        output (Union['BaseGalileoStepOutputType3', 'Document', 'Message', Unset,
            list['BaseGalileoStepOutputType7Item'], list['BaseGalileoStepOutputType8Item'], list['Document'],
            list['Message'], list[str], str]): Output of the step. Default: ''.
        root_workflow_id (Union[None, Unset, str]):
        status_code (Union[None, Unset, int]): Status code of the step. Used for logging failed/errored steps.
        step_id (Union[None, Unset, str]):
        steps (Union[None, Unset, list['BaseGalileoStep']]):
        type_ (Union[Unset, Any]): Type of the step. By default, it is set to workflow. Default: 'workflow'.
        workflow_id (Union[None, Unset, str]):
    """

    input_: Union[
        "BaseGalileoStepInputType3",
        "Document",
        "Message",
        list["BaseGalileoStepInputType7Item"],
        list["BaseGalileoStepInputType8Item"],
        list["Document"],
        list["Message"],
        list[str],
        str,
    ]
    created_at_ns: Union[Unset, int] = UNSET
    duration_ns: Union[Unset, int] = 0
    ground_truth: Union[None, Unset, str] = UNSET
    metadata: Union[Unset, "BaseGalileoStepMetadata"] = UNSET
    metrics: Union[None, Unset, list["StepMetric"]] = UNSET
    name: Union[Unset, str] = ""
    output: Union[
        "BaseGalileoStepOutputType3",
        "Document",
        "Message",
        Unset,
        list["BaseGalileoStepOutputType7Item"],
        list["BaseGalileoStepOutputType8Item"],
        list["Document"],
        list["Message"],
        list[str],
        str,
    ] = ""
    root_workflow_id: Union[None, Unset, str] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    step_id: Union[None, Unset, str] = UNSET
    steps: Union[None, Unset, list["BaseGalileoStep"]] = UNSET
    type_: Union[Unset, Any] = "workflow"
    workflow_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_galileo_step_input_type_3 import BaseGalileoStepInputType3
        from ..models.base_galileo_step_output_type_3 import BaseGalileoStepOutputType3
        from ..models.document import Document
        from ..models.message import Message

        input_: Union[dict[str, Any], list[dict[str, Any]], list[str], str]
        if isinstance(self.input_, Document):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, Message):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, BaseGalileoStepInputType3):
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

        metrics: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.metrics, Unset):
            metrics = UNSET
        elif isinstance(self.metrics, list):
            metrics = []
            for metrics_type_0_item_data in self.metrics:
                metrics_type_0_item = metrics_type_0_item_data.to_dict()
                metrics.append(metrics_type_0_item)

        else:
            metrics = self.metrics

        name = self.name

        output: Union[Unset, dict[str, Any], list[dict[str, Any]], list[str], str]
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, Document):
            output = self.output.to_dict()
        elif isinstance(self.output, Message):
            output = self.output.to_dict()
        elif isinstance(self.output, BaseGalileoStepOutputType3):
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

        root_workflow_id: Union[None, Unset, str]
        if isinstance(self.root_workflow_id, Unset):
            root_workflow_id = UNSET
        else:
            root_workflow_id = self.root_workflow_id

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        step_id: Union[None, Unset, str]
        if isinstance(self.step_id, Unset):
            step_id = UNSET
        else:
            step_id = self.step_id

        steps: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.steps, Unset):
            steps = UNSET
        elif isinstance(self.steps, list):
            steps = []
            for steps_type_0_item_data in self.steps:
                steps_type_0_item = steps_type_0_item_data.to_dict()
                steps.append(steps_type_0_item)

        else:
            steps = self.steps

        type_ = self.type_

        workflow_id: Union[None, Unset, str]
        if isinstance(self.workflow_id, Unset):
            workflow_id = UNSET
        else:
            workflow_id = self.workflow_id

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
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if name is not UNSET:
            field_dict["name"] = name
        if output is not UNSET:
            field_dict["output"] = output
        if root_workflow_id is not UNSET:
            field_dict["root_workflow_id"] = root_workflow_id
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if step_id is not UNSET:
            field_dict["step_id"] = step_id
        if steps is not UNSET:
            field_dict["steps"] = steps
        if type_ is not UNSET:
            field_dict["type"] = type_
        if workflow_id is not UNSET:
            field_dict["workflow_id"] = workflow_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.base_galileo_step_input_type_3 import BaseGalileoStepInputType3
        from ..models.base_galileo_step_input_type_7_item import BaseGalileoStepInputType7Item
        from ..models.base_galileo_step_input_type_8_item import BaseGalileoStepInputType8Item
        from ..models.base_galileo_step_metadata import BaseGalileoStepMetadata
        from ..models.base_galileo_step_output_type_3 import BaseGalileoStepOutputType3
        from ..models.base_galileo_step_output_type_7_item import BaseGalileoStepOutputType7Item
        from ..models.base_galileo_step_output_type_8_item import BaseGalileoStepOutputType8Item
        from ..models.document import Document
        from ..models.message import Message
        from ..models.step_metric import StepMetric

        d = src_dict.copy()

        def _parse_input_(
            data: object,
        ) -> Union[
            "BaseGalileoStepInputType3",
            "Document",
            "Message",
            list["BaseGalileoStepInputType7Item"],
            list["BaseGalileoStepInputType8Item"],
            list["Document"],
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
                input_type_3 = BaseGalileoStepInputType3.from_dict(data)

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
                    input_type_7_item = BaseGalileoStepInputType7Item.from_dict(input_type_7_item_data)

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
                    input_type_8_item = BaseGalileoStepInputType8Item.from_dict(input_type_8_item_data)

                    input_type_8.append(input_type_8_item)

                return input_type_8
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "BaseGalileoStepInputType3",
                    "Document",
                    "Message",
                    list["BaseGalileoStepInputType7Item"],
                    list["BaseGalileoStepInputType8Item"],
                    list["Document"],
                    list["Message"],
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
        metadata: Union[Unset, BaseGalileoStepMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = BaseGalileoStepMetadata.from_dict(_metadata)

        def _parse_metrics(data: object) -> Union[None, Unset, list["StepMetric"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                metrics_type_0 = []
                _metrics_type_0 = data
                for metrics_type_0_item_data in _metrics_type_0:
                    metrics_type_0_item = StepMetric.from_dict(metrics_type_0_item_data)

                    metrics_type_0.append(metrics_type_0_item)

                return metrics_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["StepMetric"]], data)

        metrics = _parse_metrics(d.pop("metrics", UNSET))

        name = d.pop("name", UNSET)

        def _parse_output(
            data: object,
        ) -> Union[
            "BaseGalileoStepOutputType3",
            "Document",
            "Message",
            Unset,
            list["BaseGalileoStepOutputType7Item"],
            list["BaseGalileoStepOutputType8Item"],
            list["Document"],
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
                output_type_3 = BaseGalileoStepOutputType3.from_dict(data)

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
                    output_type_7_item = BaseGalileoStepOutputType7Item.from_dict(output_type_7_item_data)

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
                    output_type_8_item = BaseGalileoStepOutputType8Item.from_dict(output_type_8_item_data)

                    output_type_8.append(output_type_8_item)

                return output_type_8
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "BaseGalileoStepOutputType3",
                    "Document",
                    "Message",
                    Unset,
                    list["BaseGalileoStepOutputType7Item"],
                    list["BaseGalileoStepOutputType8Item"],
                    list["Document"],
                    list["Message"],
                    list[str],
                    str,
                ],
                data,
            )

        output = _parse_output(d.pop("output", UNSET))

        def _parse_root_workflow_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        root_workflow_id = _parse_root_workflow_id(d.pop("root_workflow_id", UNSET))

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        def _parse_step_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        step_id = _parse_step_id(d.pop("step_id", UNSET))

        def _parse_steps(data: object) -> Union[None, Unset, list["BaseGalileoStep"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                steps_type_0 = []
                _steps_type_0 = data
                for steps_type_0_item_data in _steps_type_0:
                    steps_type_0_item = BaseGalileoStep.from_dict(steps_type_0_item_data)

                    steps_type_0.append(steps_type_0_item)

                return steps_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["BaseGalileoStep"]], data)

        steps = _parse_steps(d.pop("steps", UNSET))

        type_ = d.pop("type", UNSET)

        def _parse_workflow_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        workflow_id = _parse_workflow_id(d.pop("workflow_id", UNSET))

        base_galileo_step = cls(
            input_=input_,
            created_at_ns=created_at_ns,
            duration_ns=duration_ns,
            ground_truth=ground_truth,
            metadata=metadata,
            metrics=metrics,
            name=name,
            output=output,
            root_workflow_id=root_workflow_id,
            status_code=status_code,
            step_id=step_id,
            steps=steps,
            type_=type_,
            workflow_id=workflow_id,
        )

        base_galileo_step.additional_properties = d
        return base_galileo_step

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
