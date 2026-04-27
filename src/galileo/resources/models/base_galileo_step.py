from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_type import NodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_galileo_step_metadata import BaseGalileoStepMetadata
    from ..models.step_metric import StepMetric


T = TypeVar("T", bound="BaseGalileoStep")


@_attrs_define
class BaseGalileoStep:
    """
    Attributes:
        input_ (str): Input to the step.
        type_ (NodeType | Unset):
        redacted_input (str | Unset): Redacted input of the step. This is used to redact sensitive information.
        output (str | Unset): Output of the step.
        redacted_output (str | Unset): Redacted output of the step. This is used to redact sensitive information.
        name (str | Unset): Name of the step. Default: ''.
        created_at_ns (int | Unset): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (int | Unset): Duration of the step in nanoseconds. Default: 0.
        metadata (BaseGalileoStepMetadata | Unset): Metadata associated with this step.
        status_code (int | None | Unset): Status code of the step. Used for logging failed/errored steps.
        ground_truth (None | str | Unset): Ground truth expected output for the step.
        root_workflow_id (None | str | Unset):
        workflow_id (None | str | Unset):
        step_id (None | str | Unset):
        steps (list[BaseGalileoStep] | None | Unset):
        metrics (list[StepMetric] | Unset):
    """

    input_: str
    type_: NodeType | Unset = UNSET
    redacted_input: str | Unset = UNSET
    output: str | Unset = UNSET
    redacted_output: str | Unset = UNSET
    name: str | Unset = ""
    created_at_ns: int | Unset = UNSET
    duration_ns: int | Unset = 0
    metadata: BaseGalileoStepMetadata | Unset = UNSET
    status_code: int | None | Unset = UNSET
    ground_truth: None | str | Unset = UNSET
    root_workflow_id: None | str | Unset = UNSET
    workflow_id: None | str | Unset = UNSET
    step_id: None | str | Unset = UNSET
    steps: list[BaseGalileoStep] | None | Unset = UNSET
    metrics: list[StepMetric] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_ = self.input_

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        redacted_input = self.redacted_input

        output = self.output

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

        root_workflow_id: None | str | Unset
        if isinstance(self.root_workflow_id, Unset):
            root_workflow_id = UNSET
        else:
            root_workflow_id = self.root_workflow_id

        workflow_id: None | str | Unset
        if isinstance(self.workflow_id, Unset):
            workflow_id = UNSET
        else:
            workflow_id = self.workflow_id

        step_id: None | str | Unset
        if isinstance(self.step_id, Unset):
            step_id = UNSET
        else:
            step_id = self.step_id

        steps: list[dict[str, Any]] | None | Unset
        if isinstance(self.steps, Unset):
            steps = UNSET
        elif isinstance(self.steps, list):
            steps = []
            for steps_type_0_item_data in self.steps:
                steps_type_0_item = steps_type_0_item_data.to_dict()
                steps.append(steps_type_0_item)

        else:
            steps = self.steps

        metrics: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = []
            for metrics_item_data in self.metrics:
                metrics_item = metrics_item_data.to_dict()
                metrics.append(metrics_item)

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
        if root_workflow_id is not UNSET:
            field_dict["root_workflow_id"] = root_workflow_id
        if workflow_id is not UNSET:
            field_dict["workflow_id"] = workflow_id
        if step_id is not UNSET:
            field_dict["step_id"] = step_id
        if steps is not UNSET:
            field_dict["steps"] = steps
        if metrics is not UNSET:
            field_dict["metrics"] = metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_galileo_step_metadata import BaseGalileoStepMetadata
        from ..models.step_metric import StepMetric

        d = dict(src_dict)
        input_ = d.pop("input")

        _type_ = d.pop("type", UNSET)
        type_: NodeType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = NodeType(_type_)

        redacted_input = d.pop("redacted_input", UNSET)

        output = d.pop("output", UNSET)

        redacted_output = d.pop("redacted_output", UNSET)

        name = d.pop("name", UNSET)

        created_at_ns = d.pop("created_at_ns", UNSET)

        duration_ns = d.pop("duration_ns", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: BaseGalileoStepMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = BaseGalileoStepMetadata.from_dict(_metadata)

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

        def _parse_root_workflow_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        root_workflow_id = _parse_root_workflow_id(d.pop("root_workflow_id", UNSET))

        def _parse_workflow_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        workflow_id = _parse_workflow_id(d.pop("workflow_id", UNSET))

        def _parse_step_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        step_id = _parse_step_id(d.pop("step_id", UNSET))

        def _parse_steps(data: object) -> list[BaseGalileoStep] | None | Unset:
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
            return cast(list[BaseGalileoStep] | None | Unset, data)

        steps = _parse_steps(d.pop("steps", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: list[StepMetric] | Unset = UNSET
        if _metrics is not UNSET:
            metrics = []
            for metrics_item_data in _metrics:
                metrics_item = StepMetric.from_dict(metrics_item_data)

                metrics.append(metrics_item)

        base_galileo_step = cls(
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
            root_workflow_id=root_workflow_id,
            workflow_id=workflow_id,
            step_id=step_id,
            steps=steps,
            metrics=metrics,
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
