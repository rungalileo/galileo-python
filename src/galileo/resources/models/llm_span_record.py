import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.llm_metrics import LlmMetrics
    from ..models.llm_span_record_dataset_metadata import LlmSpanRecordDatasetMetadata
    from ..models.llm_span_record_metric_info_type_0 import LlmSpanRecordMetricInfoType0
    from ..models.llm_span_record_tools_type_0_item import LlmSpanRecordToolsType0Item
    from ..models.llm_span_record_user_metadata import LlmSpanRecordUserMetadata
    from ..models.message import Message


T = TypeVar("T", bound="LlmSpanRecord")


@_attrs_define
class LlmSpanRecord:
    """
    Attributes:
        id (str): Galileo ID of the session, trace or span
        input_ (list['Message']): Input to the trace or span.
        output (Message):
        parent_id (str): Galileo ID of the parent of this span
        project_id (str): Galileo ID of the project associated with this trace or span
        run_id (str): Galileo ID of the run (log stream or experiment) associated with this trace or span
        session_id (str): Galileo ID of the session
        trace_id (str): Galileo ID of the trace containing the span (or the same value as id for a trace)
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        dataset_input (Union[None, Unset, str]): Input to the dataset associated with this trace
        dataset_metadata (Union[Unset, LlmSpanRecordDatasetMetadata]): Metadata from the dataset associated with this
            trace
        dataset_output (Union[None, Unset, str]): Output from the dataset associated with this trace
        external_id (Union[None, Unset, str]): A user-provided session, trace or span ID.
        finish_reason (Union[None, Unset, str]): Reason for finishing.
        has_children (Union[None, Unset, bool]): Whether or not this trace or span has child spans
        is_complete (Union[Unset, bool]): Whether the parent trace is complete or not Default: True.
        metric_info (Union['LlmSpanRecordMetricInfoType0', None, Unset]): Detailed information about the metrics
            associated with this trace or span
        metrics (Union[Unset, LlmMetrics]):
        metrics_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        model (Union[None, Unset, str]): Model used for this span.
        name (Union[Unset, str]): Name of the trace, span or session. Default: ''.
        session_batch_id (Union[None, Unset, str]): Galileo ID of the metrics batch associated with this trace or span
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        step_number (Union[None, Unset, int]): Topological step number of the span.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        temperature (Union[None, Unset, float]): Temperature used for generation.
        tools (Union[None, Unset, list['LlmSpanRecordToolsType0Item']]): List of available tools passed to the LLM on
            invocation.
        type_ (Union[Literal['llm'], Unset]): Type of the trace, span or session. Default: 'llm'.
        updated_at (Union[None, Unset, datetime.datetime]): Timestamp of the session or trace or span's last update
        user_metadata (Union[Unset, LlmSpanRecordUserMetadata]): Metadata associated with this trace or span.
    """

    id: str
    input_: list["Message"]
    output: "Message"
    parent_id: str
    project_id: str
    run_id: str
    session_id: str
    trace_id: str
    created_at: Union[Unset, datetime.datetime] = UNSET
    dataset_input: Union[None, Unset, str] = UNSET
    dataset_metadata: Union[Unset, "LlmSpanRecordDatasetMetadata"] = UNSET
    dataset_output: Union[None, Unset, str] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    finish_reason: Union[None, Unset, str] = UNSET
    has_children: Union[None, Unset, bool] = UNSET
    is_complete: Union[Unset, bool] = True
    metric_info: Union["LlmSpanRecordMetricInfoType0", None, Unset] = UNSET
    metrics: Union[Unset, "LlmMetrics"] = UNSET
    metrics_batch_id: Union[None, Unset, str] = UNSET
    model: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = ""
    session_batch_id: Union[None, Unset, str] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    step_number: Union[None, Unset, int] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    temperature: Union[None, Unset, float] = UNSET
    tools: Union[None, Unset, list["LlmSpanRecordToolsType0Item"]] = UNSET
    type_: Union[Literal["llm"], Unset] = "llm"
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    user_metadata: Union[Unset, "LlmSpanRecordUserMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.llm_span_record_metric_info_type_0 import LlmSpanRecordMetricInfoType0

        id = self.id

        input_ = []
        for input_item_data in self.input_:
            input_item = input_item_data.to_dict()
            input_.append(input_item)

        output = self.output.to_dict()

        parent_id = self.parent_id

        project_id = self.project_id

        run_id = self.run_id

        session_id = self.session_id

        trace_id = self.trace_id

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        dataset_input: Union[None, Unset, str]
        if isinstance(self.dataset_input, Unset):
            dataset_input = UNSET
        else:
            dataset_input = self.dataset_input

        dataset_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.dataset_metadata, Unset):
            dataset_metadata = self.dataset_metadata.to_dict()

        dataset_output: Union[None, Unset, str]
        if isinstance(self.dataset_output, Unset):
            dataset_output = UNSET
        else:
            dataset_output = self.dataset_output

        external_id: Union[None, Unset, str]
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        finish_reason: Union[None, Unset, str]
        if isinstance(self.finish_reason, Unset):
            finish_reason = UNSET
        else:
            finish_reason = self.finish_reason

        has_children: Union[None, Unset, bool]
        if isinstance(self.has_children, Unset):
            has_children = UNSET
        else:
            has_children = self.has_children

        is_complete = self.is_complete

        metric_info: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metric_info, Unset):
            metric_info = UNSET
        elif isinstance(self.metric_info, LlmSpanRecordMetricInfoType0):
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

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        name = self.name

        session_batch_id: Union[None, Unset, str]
        if isinstance(self.session_batch_id, Unset):
            session_batch_id = UNSET
        else:
            session_batch_id = self.session_batch_id

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        step_number: Union[None, Unset, int]
        if isinstance(self.step_number, Unset):
            step_number = UNSET
        else:
            step_number = self.step_number

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

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
                "output": output,
                "parent_id": parent_id,
                "project_id": project_id,
                "run_id": run_id,
                "session_id": session_id,
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
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if finish_reason is not UNSET:
            field_dict["finish_reason"] = finish_reason
        if has_children is not UNSET:
            field_dict["has_children"] = has_children
        if is_complete is not UNSET:
            field_dict["is_complete"] = is_complete
        if metric_info is not UNSET:
            field_dict["metric_info"] = metric_info
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if metrics_batch_id is not UNSET:
            field_dict["metrics_batch_id"] = metrics_batch_id
        if model is not UNSET:
            field_dict["model"] = model
        if name is not UNSET:
            field_dict["name"] = name
        if session_batch_id is not UNSET:
            field_dict["session_batch_id"] = session_batch_id
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if step_number is not UNSET:
            field_dict["step_number"] = step_number
        if tags is not UNSET:
            field_dict["tags"] = tags
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if tools is not UNSET:
            field_dict["tools"] = tools
        if type_ is not UNSET:
            field_dict["type"] = type_
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.llm_metrics import LlmMetrics
        from ..models.llm_span_record_dataset_metadata import LlmSpanRecordDatasetMetadata
        from ..models.llm_span_record_metric_info_type_0 import LlmSpanRecordMetricInfoType0
        from ..models.llm_span_record_tools_type_0_item import LlmSpanRecordToolsType0Item
        from ..models.llm_span_record_user_metadata import LlmSpanRecordUserMetadata
        from ..models.message import Message

        d = dict(src_dict)
        id = d.pop("id")

        input_ = []
        _input_ = d.pop("input")
        for input_item_data in _input_:
            input_item = Message.from_dict(input_item_data)

            input_.append(input_item)

        output = Message.from_dict(d.pop("output"))

        parent_id = d.pop("parent_id")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        session_id = d.pop("session_id")

        trace_id = d.pop("trace_id")

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        def _parse_dataset_input(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_input = _parse_dataset_input(d.pop("dataset_input", UNSET))

        _dataset_metadata = d.pop("dataset_metadata", UNSET)
        dataset_metadata: Union[Unset, LlmSpanRecordDatasetMetadata]
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = LlmSpanRecordDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_dataset_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_output = _parse_dataset_output(d.pop("dataset_output", UNSET))

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_finish_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        finish_reason = _parse_finish_reason(d.pop("finish_reason", UNSET))

        def _parse_has_children(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        has_children = _parse_has_children(d.pop("has_children", UNSET))

        is_complete = d.pop("is_complete", UNSET)

        def _parse_metric_info(data: object) -> Union["LlmSpanRecordMetricInfoType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_info_type_0 = LlmSpanRecordMetricInfoType0.from_dict(data)

                return metric_info_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LlmSpanRecordMetricInfoType0", None, Unset], data)

        metric_info = _parse_metric_info(d.pop("metric_info", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, LlmMetrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = LlmMetrics.from_dict(_metrics)

        def _parse_metrics_batch_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metrics_batch_id = _parse_metrics_batch_id(d.pop("metrics_batch_id", UNSET))

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        name = d.pop("name", UNSET)

        def _parse_session_batch_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_batch_id = _parse_session_batch_id(d.pop("session_batch_id", UNSET))

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        def _parse_step_number(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        step_number = _parse_step_number(d.pop("step_number", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_tools(data: object) -> Union[None, Unset, list["LlmSpanRecordToolsType0Item"]]:
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
                    tools_type_0_item = LlmSpanRecordToolsType0Item.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["LlmSpanRecordToolsType0Item"]], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        type_ = cast(Union[Literal["llm"], Unset], d.pop("type", UNSET))
        if type_ != "llm" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'llm', got '{type_}'")

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
        user_metadata: Union[Unset, LlmSpanRecordUserMetadata]
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = LlmSpanRecordUserMetadata.from_dict(_user_metadata)

        llm_span_record = cls(
            id=id,
            input_=input_,
            output=output,
            parent_id=parent_id,
            project_id=project_id,
            run_id=run_id,
            session_id=session_id,
            trace_id=trace_id,
            created_at=created_at,
            dataset_input=dataset_input,
            dataset_metadata=dataset_metadata,
            dataset_output=dataset_output,
            external_id=external_id,
            finish_reason=finish_reason,
            has_children=has_children,
            is_complete=is_complete,
            metric_info=metric_info,
            metrics=metrics,
            metrics_batch_id=metrics_batch_id,
            model=model,
            name=name,
            session_batch_id=session_batch_id,
            status_code=status_code,
            step_number=step_number,
            tags=tags,
            temperature=temperature,
            tools=tools,
            type_=type_,
            updated_at=updated_at,
            user_metadata=user_metadata,
        )

        llm_span_record.additional_properties = d
        return llm_span_record

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
