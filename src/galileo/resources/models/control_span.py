import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.control_applies_to import ControlAppliesTo
from ..models.control_check_stage import ControlCheckStage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.control_result import ControlResult
    from ..models.control_span_dataset_metadata import ControlSpanDatasetMetadata
    from ..models.control_span_user_metadata import ControlSpanUserMetadata
    from ..models.file_content_part import FileContentPart
    from ..models.message import Message
    from ..models.metrics import Metrics
    from ..models.text_content_part import TextContentPart


T = TypeVar("T", bound="ControlSpan")


@_attrs_define
class ControlSpan:
    """
    Attributes
    ----------
        type_ (Union[Literal['control'], Unset]): Type of the trace, span or session. Default: 'control'.
        input_ (Union[Unset, list['Message'], list[Union['FileContentPart', 'TextContentPart']], str]): Input to the
            trace or span. Default: ''.
        redacted_input (Union[None, Unset, list['Message'], list[Union['FileContentPart', 'TextContentPart']], str]):
            Redacted input of the trace or span.
        output (Union['ControlResult', None, Unset]): Output of the trace or span.
        redacted_output (Union['ControlResult', None, Unset]): Redacted output of the trace or span.
        name (Union[Unset, str]): Name of the trace, span or session. Default: ''.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the trace or span's creation.
        user_metadata (Union[Unset, ControlSpanUserMetadata]): Metadata associated with this trace or span.
        tags (Union[Unset, list[str]]): Tags associated with this trace or span.
        status_code (Union[None, Unset, int]): Status code of the trace or span. Used for logging failure or error
            states.
        metrics (Union[Unset, Metrics]):
        external_id (Union[None, Unset, str]): A user-provided session, trace or span ID.
        dataset_input (Union[None, Unset, str]): Input to the dataset associated with this trace
        dataset_output (Union[None, Unset, str]): Output from the dataset associated with this trace
        dataset_metadata (Union[Unset, ControlSpanDatasetMetadata]): Metadata from the dataset associated with this
            trace
        id (Union[None, Unset, str]): Galileo ID of the session, trace or span
        session_id (Union[None, Unset, str]): Galileo ID of the session containing the trace or span or session
        trace_id (Union[None, Unset, str]): Galileo ID of the trace containing the span (or the same value as id for a
            trace)
        step_number (Union[None, Unset, int]): Topological step number of the span.
        parent_id (Union[None, Unset, str]): Galileo ID of the parent of this span
        control_id (Union[None, Unset, int]): Identifier of the control definition that produced this span.
        agent_name (Union[None, Unset, str]): Normalized agent name associated with this control execution.
        check_stage (Union[ControlCheckStage, None, Unset]): Execution stage where the control ran, typically 'pre' or
            'post'.
        applies_to (Union[ControlAppliesTo, None, Unset]): Parent execution type the control applied to, for example
            'llm_call' or 'tool_call'.
        evaluator_name (Union[None, Unset, str]): Representative evaluator name for this control span. For composite
            controls, this is the primary evaluator chosen for observability identity.
        selector_path (Union[None, Unset, str]): Representative selector path for this control span. For composite
            controls, this is the primary selector path chosen for observability identity.
    """

    type_: Literal["control"] | Unset = "control"
    input_: Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str = ""
    redacted_input: None | Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str = UNSET
    output: Union["ControlResult", None, Unset] = UNSET
    redacted_output: Union["ControlResult", None, Unset] = UNSET
    name: Unset | str = ""
    created_at: Unset | datetime.datetime = UNSET
    user_metadata: Union[Unset, "ControlSpanUserMetadata"] = UNSET
    tags: Unset | list[str] = UNSET
    status_code: None | Unset | int = UNSET
    metrics: Union[Unset, "Metrics"] = UNSET
    external_id: None | Unset | str = UNSET
    dataset_input: None | Unset | str = UNSET
    dataset_output: None | Unset | str = UNSET
    dataset_metadata: Union[Unset, "ControlSpanDatasetMetadata"] = UNSET
    id: None | Unset | str = UNSET
    session_id: None | Unset | str = UNSET
    trace_id: None | Unset | str = UNSET
    step_number: None | Unset | int = UNSET
    parent_id: None | Unset | str = UNSET
    control_id: None | Unset | int = UNSET
    agent_name: None | Unset | str = UNSET
    check_stage: ControlCheckStage | None | Unset = UNSET
    applies_to: ControlAppliesTo | None | Unset = UNSET
    evaluator_name: None | Unset | str = UNSET
    selector_path: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.control_result import ControlResult
        from ..models.text_content_part import TextContentPart

        type_ = self.type_

        input_: Unset | list[dict[str, Any]] | str
        if isinstance(self.input_, Unset):
            input_ = UNSET
        elif isinstance(self.input_, list):
            input_ = []
            for input_type_1_item_data in self.input_:
                input_type_1_item = input_type_1_item_data.to_dict()
                input_.append(input_type_1_item)

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_2_item_data in self.input_:
                input_type_2_item: dict[str, Any]
                if isinstance(input_type_2_item_data, TextContentPart):
                    input_type_2_item = input_type_2_item_data.to_dict()
                else:
                    input_type_2_item = input_type_2_item_data.to_dict()

                input_.append(input_type_2_item)

        else:
            input_ = self.input_

        redacted_input: None | Unset | list[dict[str, Any]] | str
        if isinstance(self.redacted_input, Unset):
            redacted_input = UNSET
        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_1_item_data in self.redacted_input:
                redacted_input_type_1_item = redacted_input_type_1_item_data.to_dict()
                redacted_input.append(redacted_input_type_1_item)

        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_2_item_data in self.redacted_input:
                redacted_input_type_2_item: dict[str, Any]
                if isinstance(redacted_input_type_2_item_data, TextContentPart):
                    redacted_input_type_2_item = redacted_input_type_2_item_data.to_dict()
                else:
                    redacted_input_type_2_item = redacted_input_type_2_item_data.to_dict()

                redacted_input.append(redacted_input_type_2_item)

        else:
            redacted_input = self.redacted_input

        output: None | Unset | dict[str, Any]
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, ControlResult):
            output = self.output.to_dict()
        else:
            output = self.output

        redacted_output: None | Unset | dict[str, Any]
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        elif isinstance(self.redacted_output, ControlResult):
            redacted_output = self.redacted_output.to_dict()
        else:
            redacted_output = self.redacted_output

        name = self.name

        created_at: Unset | str = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        user_metadata: Unset | dict[str, Any] = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        tags: Unset | list[str] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        status_code: None | Unset | int
        status_code = UNSET if isinstance(self.status_code, Unset) else self.status_code

        metrics: Unset | dict[str, Any] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        external_id: None | Unset | str
        external_id = UNSET if isinstance(self.external_id, Unset) else self.external_id

        dataset_input: None | Unset | str
        dataset_input = UNSET if isinstance(self.dataset_input, Unset) else self.dataset_input

        dataset_output: None | Unset | str
        dataset_output = UNSET if isinstance(self.dataset_output, Unset) else self.dataset_output

        dataset_metadata: Unset | dict[str, Any] = UNSET
        if not isinstance(self.dataset_metadata, Unset):
            dataset_metadata = self.dataset_metadata.to_dict()

        id: None | Unset | str
        id = UNSET if isinstance(self.id, Unset) else self.id

        session_id: None | Unset | str
        session_id = UNSET if isinstance(self.session_id, Unset) else self.session_id

        trace_id: None | Unset | str
        trace_id = UNSET if isinstance(self.trace_id, Unset) else self.trace_id

        step_number: None | Unset | int
        step_number = UNSET if isinstance(self.step_number, Unset) else self.step_number

        parent_id: None | Unset | str
        parent_id = UNSET if isinstance(self.parent_id, Unset) else self.parent_id

        control_id: None | Unset | int
        control_id = UNSET if isinstance(self.control_id, Unset) else self.control_id

        agent_name: None | Unset | str
        agent_name = UNSET if isinstance(self.agent_name, Unset) else self.agent_name

        check_stage: None | Unset | str
        if isinstance(self.check_stage, Unset):
            check_stage = UNSET
        elif isinstance(self.check_stage, ControlCheckStage):
            check_stage = self.check_stage.value
        else:
            check_stage = self.check_stage

        applies_to: None | Unset | str
        if isinstance(self.applies_to, Unset):
            applies_to = UNSET
        elif isinstance(self.applies_to, ControlAppliesTo):
            applies_to = self.applies_to.value
        else:
            applies_to = self.applies_to

        evaluator_name: None | Unset | str
        evaluator_name = UNSET if isinstance(self.evaluator_name, Unset) else self.evaluator_name

        selector_path: None | Unset | str
        selector_path = UNSET if isinstance(self.selector_path, Unset) else self.selector_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if input_ is not UNSET:
            field_dict["input"] = input_
        if redacted_input is not UNSET:
            field_dict["redacted_input"] = redacted_input
        if output is not UNSET:
            field_dict["output"] = output
        if redacted_output is not UNSET:
            field_dict["redacted_output"] = redacted_output
        if name is not UNSET:
            field_dict["name"] = name
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata
        if tags is not UNSET:
            field_dict["tags"] = tags
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if dataset_input is not UNSET:
            field_dict["dataset_input"] = dataset_input
        if dataset_output is not UNSET:
            field_dict["dataset_output"] = dataset_output
        if dataset_metadata is not UNSET:
            field_dict["dataset_metadata"] = dataset_metadata
        if id is not UNSET:
            field_dict["id"] = id
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if trace_id is not UNSET:
            field_dict["trace_id"] = trace_id
        if step_number is not UNSET:
            field_dict["step_number"] = step_number
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if control_id is not UNSET:
            field_dict["control_id"] = control_id
        if agent_name is not UNSET:
            field_dict["agent_name"] = agent_name
        if check_stage is not UNSET:
            field_dict["check_stage"] = check_stage
        if applies_to is not UNSET:
            field_dict["applies_to"] = applies_to
        if evaluator_name is not UNSET:
            field_dict["evaluator_name"] = evaluator_name
        if selector_path is not UNSET:
            field_dict["selector_path"] = selector_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.control_result import ControlResult
        from ..models.control_span_dataset_metadata import ControlSpanDatasetMetadata
        from ..models.control_span_user_metadata import ControlSpanUserMetadata
        from ..models.file_content_part import FileContentPart
        from ..models.message import Message
        from ..models.metrics import Metrics
        from ..models.text_content_part import TextContentPart

        d = dict(src_dict)
        type_ = cast(Literal["control"] | Unset, d.pop("type", UNSET))
        if type_ != "control" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'control', got '{type_}'")

        def _parse_input_(
            data: object,
        ) -> Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str:
            if isinstance(data, Unset):
                return data
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
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_2 = []
                _input_type_2 = data
                for input_type_2_item_data in _input_type_2:

                    def _parse_input_type_2_item(data: object) -> Union["FileContentPart", "TextContentPart"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return TextContentPart.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return FileContentPart.from_dict(data)

                    input_type_2_item = _parse_input_type_2_item(input_type_2_item_data)

                    input_type_2.append(input_type_2_item)

                return input_type_2
            except:  # noqa: E722
                pass
            return cast(Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str, data)

        input_ = _parse_input_(d.pop("input", UNSET))

        def _parse_redacted_input(
            data: object,
        ) -> None | Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_1 = []
                _redacted_input_type_1 = data
                for redacted_input_type_1_item_data in _redacted_input_type_1:
                    redacted_input_type_1_item = Message.from_dict(redacted_input_type_1_item_data)

                    redacted_input_type_1.append(redacted_input_type_1_item)

                return redacted_input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_2 = []
                _redacted_input_type_2 = data
                for redacted_input_type_2_item_data in _redacted_input_type_2:

                    def _parse_redacted_input_type_2_item(data: object) -> Union["FileContentPart", "TextContentPart"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return TextContentPart.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return FileContentPart.from_dict(data)

                    redacted_input_type_2_item = _parse_redacted_input_type_2_item(redacted_input_type_2_item_data)

                    redacted_input_type_2.append(redacted_input_type_2_item)

                return redacted_input_type_2
            except:  # noqa: E722
                pass
            return cast(None | Unset | list["Message"] | list[Union["FileContentPart", "TextContentPart"]] | str, data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        def _parse_output(data: object) -> Union["ControlResult", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ControlResult.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ControlResult", None, Unset], data)

        output = _parse_output(d.pop("output", UNSET))

        def _parse_redacted_output(data: object) -> Union["ControlResult", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ControlResult.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ControlResult", None, Unset], data)

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Unset | datetime.datetime
        created_at = UNSET if isinstance(_created_at, Unset) else isoparse(_created_at)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: Unset | ControlSpanUserMetadata
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = ControlSpanUserMetadata.from_dict(_user_metadata)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_status_code(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Unset | Metrics
        metrics = UNSET if isinstance(_metrics, Unset) else Metrics.from_dict(_metrics)

        def _parse_external_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_dataset_input(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        dataset_input = _parse_dataset_input(d.pop("dataset_input", UNSET))

        def _parse_dataset_output(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        dataset_output = _parse_dataset_output(d.pop("dataset_output", UNSET))

        _dataset_metadata = d.pop("dataset_metadata", UNSET)
        dataset_metadata: Unset | ControlSpanDatasetMetadata
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = ControlSpanDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_session_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_trace_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        trace_id = _parse_trace_id(d.pop("trace_id", UNSET))

        def _parse_step_number(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        step_number = _parse_step_number(d.pop("step_number", UNSET))

        def _parse_parent_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        parent_id = _parse_parent_id(d.pop("parent_id", UNSET))

        def _parse_control_id(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        control_id = _parse_control_id(d.pop("control_id", UNSET))

        def _parse_agent_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        agent_name = _parse_agent_name(d.pop("agent_name", UNSET))

        def _parse_check_stage(data: object) -> ControlCheckStage | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ControlCheckStage(data)

            except:  # noqa: E722
                pass
            return cast(ControlCheckStage | None | Unset, data)

        check_stage = _parse_check_stage(d.pop("check_stage", UNSET))

        def _parse_applies_to(data: object) -> ControlAppliesTo | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ControlAppliesTo(data)

            except:  # noqa: E722
                pass
            return cast(ControlAppliesTo | None | Unset, data)

        applies_to = _parse_applies_to(d.pop("applies_to", UNSET))

        def _parse_evaluator_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        evaluator_name = _parse_evaluator_name(d.pop("evaluator_name", UNSET))

        def _parse_selector_path(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        selector_path = _parse_selector_path(d.pop("selector_path", UNSET))

        control_span = cls(
            type_=type_,
            input_=input_,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=created_at,
            user_metadata=user_metadata,
            tags=tags,
            status_code=status_code,
            metrics=metrics,
            external_id=external_id,
            dataset_input=dataset_input,
            dataset_output=dataset_output,
            dataset_metadata=dataset_metadata,
            id=id,
            session_id=session_id,
            trace_id=trace_id,
            step_number=step_number,
            parent_id=parent_id,
            control_id=control_id,
            agent_name=agent_name,
            check_stage=check_stage,
            applies_to=applies_to,
            evaluator_name=evaluator_name,
            selector_path=selector_path,
        )

        control_span.additional_properties = d
        return control_span

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
