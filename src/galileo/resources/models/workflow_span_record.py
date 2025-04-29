import datetime
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.message import Message
    from ..models.metrics import Metrics
    from ..models.workflow_span_record_dataset_metadata import WorkflowSpanRecordDatasetMetadata
    from ..models.workflow_span_record_metric_info_type_0 import WorkflowSpanRecordMetricInfoType0
    from ..models.workflow_span_record_user_metadata import WorkflowSpanRecordUserMetadata


T = TypeVar("T", bound="WorkflowSpanRecord")


@_attrs_define
class WorkflowSpanRecord:
    """
    Attributes:
        id (str): Galileo ID of the trace or span
        input_ (Union[list['Message'], str]): Input to the trace or span.
        parent_id (str): Galileo ID of the parent of this span
        project_id (str): Galileo ID of the project associated with this trace or span
        run_id (str): Galileo ID of the run (log stream or experiment) associated with this trace or span
        trace_id (str): Galileo ID of the trace containing the span (or the same value as id for a trace)
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        dataset_input (Union[Unset, str]): Input to the dataset associated with this trace Default: ''.
        dataset_metadata (Union[Unset, WorkflowSpanRecordDatasetMetadata]): Metadata from the dataset associated with
            this trace
        dataset_output (Union[Unset, str]): Output from the dataset associated with this trace Default: ''.
        has_children (Union[None, Unset, bool]): Whether or not this trace or span has child spans
        metric_info (Union['WorkflowSpanRecordMetricInfoType0', None, Unset]): Detailed information about the metrics
            associated with this trace or span
        metrics (Union[Unset, Metrics]):
        metrics_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        name (Union[Unset, str]): Name of the trace or span. Default: ''.
        output (Union['Message', None, Unset, list['Document'], str]): Output of the trace or span.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        type_ (Union[Literal['workflow'], Unset]): Type of the trace or span. Default: 'workflow'.
        updated_at (Union[None, Unset, datetime.datetime]): Timestamp of the trace or span's last update
        user_metadata (Union[Unset, WorkflowSpanRecordUserMetadata]): Metadata associated with this trace or span.
    """

    id: str
    input_: Union[list["Message"], str]
    parent_id: str
    project_id: str
    run_id: str
    trace_id: str
    created_at: Union[Unset, datetime.datetime] = UNSET
    dataset_input: Union[Unset, str] = ""
    dataset_metadata: Union[Unset, "WorkflowSpanRecordDatasetMetadata"] = UNSET
    dataset_output: Union[Unset, str] = ""
    has_children: Union[None, Unset, bool] = UNSET
    metric_info: Union["WorkflowSpanRecordMetricInfoType0", None, Unset] = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    metrics_batch_id: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = ""
    output: Union["Message", None, Unset, list["Document"], str] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    type_: Union[Literal["workflow"], Unset] = "workflow"
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    user_metadata: Union[Unset, "WorkflowSpanRecordUserMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.message import Message
        from ..models.workflow_span_record_metric_info_type_0 import WorkflowSpanRecordMetricInfoType0

        id = self.id

        input_: Union[list[dict[str, Any]], str]
        if isinstance(self.input_, list):
            input_ = []
            for input_type_1_item_data in self.input_:
                input_type_1_item = input_type_1_item_data.to_dict()
                input_.append(input_type_1_item)

        else:
            input_ = self.input_

        parent_id = self.parent_id

        project_id = self.project_id

        run_id = self.run_id

        trace_id = self.trace_id

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        dataset_input = self.dataset_input

        dataset_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.dataset_metadata, Unset):
            dataset_metadata = self.dataset_metadata.to_dict()

        dataset_output = self.dataset_output

        has_children: Union[None, Unset, bool]
        if isinstance(self.has_children, Unset):
            has_children = UNSET
        else:
            has_children = self.has_children

        metric_info: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metric_info, Unset):
            metric_info = UNSET
        elif isinstance(self.metric_info, WorkflowSpanRecordMetricInfoType0):
            metric_info = self.metric_info.to_dict()
        else:
            metric_info = self.metric_info

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        metrics_batch_id: Union[None, Unset, str]
        if isinstance(self.metrics_batch_id, Unset):
            metrics_batch_id = UNSET
        else:
            metrics_batch_id = self.metrics_batch_id

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

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        type_ = self.type_

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        user_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "input": input_,
                "parent_id": parent_id,
                "project_id": project_id,
                "run_id": run_id,
                "trace_id": trace_id,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if dataset_input is not UNSET:
            field_dict["dataset_input"] = dataset_input
        if dataset_metadata is not UNSET:
            field_dict["dataset_metadata"] = dataset_metadata
        if dataset_output is not UNSET:
            field_dict["dataset_output"] = dataset_output
        if has_children is not UNSET:
            field_dict["has_children"] = has_children
        if metric_info is not UNSET:
            field_dict["metric_info"] = metric_info
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if metrics_batch_id is not UNSET:
            field_dict["metrics_batch_id"] = metrics_batch_id
        if name is not UNSET:
            field_dict["name"] = name
        if output is not UNSET:
            field_dict["output"] = output
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type_ is not UNSET:
            field_dict["type"] = type_
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document import Document
        from ..models.message import Message
        from ..models.metrics import Metrics
        from ..models.workflow_span_record_dataset_metadata import WorkflowSpanRecordDatasetMetadata
        from ..models.workflow_span_record_metric_info_type_0 import WorkflowSpanRecordMetricInfoType0
        from ..models.workflow_span_record_user_metadata import WorkflowSpanRecordUserMetadata

        d = src_dict.copy()
        id = d.pop("id")

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

        parent_id = d.pop("parent_id")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        trace_id = d.pop("trace_id")

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        dataset_input = d.pop("dataset_input", UNSET)

        _dataset_metadata = d.pop("dataset_metadata", UNSET)
        dataset_metadata: Union[Unset, WorkflowSpanRecordDatasetMetadata]
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = WorkflowSpanRecordDatasetMetadata.from_dict(_dataset_metadata)

        dataset_output = d.pop("dataset_output", UNSET)

        def _parse_has_children(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        has_children = _parse_has_children(d.pop("has_children", UNSET))

        def _parse_metric_info(data: object) -> Union["WorkflowSpanRecordMetricInfoType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_info_type_0 = WorkflowSpanRecordMetricInfoType0.from_dict(data)

                return metric_info_type_0
            except:  # noqa: E722
                pass
            return cast(Union["WorkflowSpanRecordMetricInfoType0", None, Unset], data)

        metric_info = _parse_metric_info(d.pop("metric_info", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, Metrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = Metrics.from_dict(_metrics)

        def _parse_metrics_batch_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metrics_batch_id = _parse_metrics_batch_id(d.pop("metrics_batch_id", UNSET))

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

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Union[Unset, WorkflowSpanRecordUserMetadata]
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = WorkflowSpanRecordUserMetadata.from_dict(_user_metadata)

        workflow_span_record = cls(
            id=id,
            input_=input_,
            parent_id=parent_id,
            project_id=project_id,
            run_id=run_id,
            trace_id=trace_id,
            created_at=created_at,
            dataset_input=dataset_input,
            dataset_metadata=dataset_metadata,
            dataset_output=dataset_output,
            has_children=has_children,
            metric_info=metric_info,
            metrics=metrics,
            metrics_batch_id=metrics_batch_id,
            name=name,
            output=output,
            status_code=status_code,
            tags=tags,
            type_=type_,
            updated_at=updated_at,
            user_metadata=user_metadata,
        )

        workflow_span_record.additional_properties = d
        return workflow_span_record

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
