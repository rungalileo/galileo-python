from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
    from ..models.extended_control_span_record import ExtendedControlSpanRecord
    from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
    from ..models.extended_retriever_span_record_with_children import ExtendedRetrieverSpanRecordWithChildren
    from ..models.extended_tool_span_record_with_children import ExtendedToolSpanRecordWithChildren
    from ..models.extended_workflow_span_record_with_children import ExtendedWorkflowSpanRecordWithChildren


T = TypeVar("T", bound="StubTraceRecord")


@_attrs_define
class StubTraceRecord:
    """Placeholder for a trace referenced by spans but not yet ingested.

    Synthesized when one or more spans declare trace_id=X but no
    TraceRecord with that id exists in storage. Holds the orphan spans
    together so the client can render them under a single root.

    Extends ExtendedRecordWithChildSpans so isinstance checks work
    uniformly for both real and stub traces.

    Attributes
    ----------
            id (str): ID of the missing trace, taken from span trace_id references.
            spans (Union[Unset, list[Union['ExtendedAgentSpanRecordWithChildren', 'ExtendedControlSpanRecord',
                'ExtendedLlmSpanRecord', 'ExtendedRetrieverSpanRecordWithChildren', 'ExtendedToolSpanRecordWithChildren',
                'ExtendedWorkflowSpanRecordWithChildren']]]):
            type_ (Union[Literal['stub_trace'], Unset]): Discriminator; identifies this as a synthesized placeholder, not a
                real trace. Default: 'stub_trace'.
            project_id (Union[None, Unset, str]): Project ID inferred from child spans, if all agree; otherwise None.
            run_id (Union[None, Unset, str]): Run ID inferred from child spans, if all agree; otherwise None.
            session_id (Union[None, Unset, str]): Session ID inferred from child spans, if all agree; otherwise None.
    """

    id: str
    spans: (
        Unset
        | list[
            Union[
                "ExtendedAgentSpanRecordWithChildren",
                "ExtendedControlSpanRecord",
                "ExtendedLlmSpanRecord",
                "ExtendedRetrieverSpanRecordWithChildren",
                "ExtendedToolSpanRecordWithChildren",
                "ExtendedWorkflowSpanRecordWithChildren",
            ]
        ]
    ) = UNSET
    type_: Literal["stub_trace"] | Unset = "stub_trace"
    project_id: None | Unset | str = UNSET
    run_id: None | Unset | str = UNSET
    session_id: None | Unset | str = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
        from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
        from ..models.extended_retriever_span_record_with_children import ExtendedRetrieverSpanRecordWithChildren
        from ..models.extended_tool_span_record_with_children import ExtendedToolSpanRecordWithChildren
        from ..models.extended_workflow_span_record_with_children import ExtendedWorkflowSpanRecordWithChildren

        id = self.id

        spans: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.spans, Unset):
            spans = []
            for spans_item_data in self.spans:
                spans_item: dict[str, Any]
                if isinstance(
                    spans_item_data,
                    ExtendedAgentSpanRecordWithChildren
                    | ExtendedWorkflowSpanRecordWithChildren
                    | ExtendedLlmSpanRecord
                    | ExtendedToolSpanRecordWithChildren
                    | ExtendedRetrieverSpanRecordWithChildren,
                ):
                    spans_item = spans_item_data.to_dict()
                else:
                    spans_item = spans_item_data.to_dict()

                spans.append(spans_item)

        type_ = self.type_

        project_id: None | Unset | str
        project_id = UNSET if isinstance(self.project_id, Unset) else self.project_id

        run_id: None | Unset | str
        run_id = UNSET if isinstance(self.run_id, Unset) else self.run_id

        session_id: None | Unset | str
        session_id = UNSET if isinstance(self.session_id, Unset) else self.session_id

        field_dict: dict[str, Any] = {}

        field_dict.update({"id": id})
        if spans is not UNSET:
            field_dict["spans"] = spans
        if type_ is not UNSET:
            field_dict["type"] = type_
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if run_id is not UNSET:
            field_dict["run_id"] = run_id
        if session_id is not UNSET:
            field_dict["session_id"] = session_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
        from ..models.extended_control_span_record import ExtendedControlSpanRecord
        from ..models.extended_retriever_span_record_with_children import ExtendedRetrieverSpanRecordWithChildren
        from ..models.extended_tool_span_record_with_children import ExtendedToolSpanRecordWithChildren
        from ..models.extended_workflow_span_record_with_children import ExtendedWorkflowSpanRecordWithChildren

        d = dict(src_dict)
        id = d.pop("id")

        spans = []
        _spans = d.pop("spans", UNSET)
        for spans_item_data in _spans or []:

            def _parse_spans_item(
                data: object,
            ) -> Union[
                "ExtendedAgentSpanRecordWithChildren",
                "ExtendedControlSpanRecord",
                "ExtendedLlmSpanRecord",
                "ExtendedRetrieverSpanRecordWithChildren",
                "ExtendedToolSpanRecordWithChildren",
                "ExtendedWorkflowSpanRecordWithChildren",
            ]:
                # Discriminator-aware parsing for Extended*Record types
                if isinstance(data, dict) and "type" in data:
                    type_value = data.get("type")

                    # Hardcoded discriminator mapping for Extended*Record types
                    if type_value == "trace":
                        try:
                            from ..models.extended_trace_record import ExtendedTraceRecord

                            return ExtendedTraceRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "agent":
                        try:
                            from ..models.extended_agent_span_record import ExtendedAgentSpanRecord

                            return ExtendedAgentSpanRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "workflow":
                        try:
                            from ..models.extended_workflow_span_record import ExtendedWorkflowSpanRecord

                            return ExtendedWorkflowSpanRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "llm":
                        try:
                            from ..models.extended_llm_span_record import ExtendedLlmSpanRecord

                            return ExtendedLlmSpanRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "tool":
                        try:
                            from ..models.extended_tool_span_record import ExtendedToolSpanRecord

                            return ExtendedToolSpanRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "retriever":
                        try:
                            from ..models.extended_retriever_span_record import ExtendedRetrieverSpanRecord

                            return ExtendedRetrieverSpanRecord.from_dict(data)
                        except:  # noqa: E722
                            pass
                    elif type_value == "session":
                        try:
                            from ..models.extended_session_record import ExtendedSessionRecord

                            return ExtendedSessionRecord.from_dict(data)
                        except:  # noqa: E722
                            pass

                # Fallback to standard union parsing
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedAgentSpanRecordWithChildren.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedWorkflowSpanRecordWithChildren.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedLlmSpanRecord.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedToolSpanRecordWithChildren.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedRetrieverSpanRecordWithChildren.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedControlSpanRecord.from_dict(data)

                except:  # noqa: E722
                    pass
                # If we reach here, none of the parsers succeeded
                discriminator_info = f" (type={data.get('type')})" if isinstance(data, dict) and "type" in data else ""
                raise ValueError(f"Could not parse union type for spans_item{discriminator_info}")

            spans_item = _parse_spans_item(spans_item_data)

            spans.append(spans_item)

        type_ = cast(Literal["stub_trace"] | Unset, d.pop("type", UNSET))
        if type_ != "stub_trace" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'stub_trace', got '{type_}'")

        def _parse_project_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_run_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        def _parse_session_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        return cls(id=id, spans=spans, type_=type_, project_id=project_id, run_id=run_id, session_id=session_id)
