from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extended_agent_span_record import ExtendedAgentSpanRecord
    from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
    from ..models.extended_retriever_span_record import ExtendedRetrieverSpanRecord
    from ..models.extended_session_record import ExtendedSessionRecord
    from ..models.extended_tool_span_record import ExtendedToolSpanRecord
    from ..models.extended_trace_record import ExtendedTraceRecord
    from ..models.extended_workflow_span_record import ExtendedWorkflowSpanRecord


T = TypeVar("T", bound="LogRecordsQueryResponse")


@_attrs_define
class LogRecordsQueryResponse:
    """
    Attributes:
        limit (Union[Unset, int]):  Default: 100.
        next_starting_token (Union[None, Unset, int]):
        paginated (Union[Unset, bool]):  Default: False.
        records (Union[Unset, list[Union['ExtendedAgentSpanRecord', 'ExtendedLlmSpanRecord',
            'ExtendedRetrieverSpanRecord', 'ExtendedSessionRecord', 'ExtendedToolSpanRecord', 'ExtendedTraceRecord',
            'ExtendedWorkflowSpanRecord']]]): records matching the query
        starting_token (Union[Unset, int]):  Default: 0.
    """

    limit: Union[Unset, int] = 100
    next_starting_token: Union[None, Unset, int] = UNSET
    paginated: Union[Unset, bool] = False
    records: Union[
        Unset,
        list[
            Union[
                "ExtendedAgentSpanRecord",
                "ExtendedLlmSpanRecord",
                "ExtendedRetrieverSpanRecord",
                "ExtendedSessionRecord",
                "ExtendedToolSpanRecord",
                "ExtendedTraceRecord",
                "ExtendedWorkflowSpanRecord",
            ]
        ],
    ] = UNSET
    starting_token: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.extended_agent_span_record import ExtendedAgentSpanRecord
        from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
        from ..models.extended_retriever_span_record import ExtendedRetrieverSpanRecord
        from ..models.extended_tool_span_record import ExtendedToolSpanRecord
        from ..models.extended_trace_record import ExtendedTraceRecord
        from ..models.extended_workflow_span_record import ExtendedWorkflowSpanRecord

        limit = self.limit

        next_starting_token: Union[None, Unset, int]
        next_starting_token = UNSET if isinstance(self.next_starting_token, Unset) else self.next_starting_token

        paginated = self.paginated

        records: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.records, Unset):
            records = []
            for records_item_data in self.records:
                records_item: dict[str, Any]
                if isinstance(
                    records_item_data,
                    (
                        ExtendedTraceRecord,
                        ExtendedAgentSpanRecord,
                        ExtendedWorkflowSpanRecord,
                        ExtendedLlmSpanRecord,
                        ExtendedToolSpanRecord,
                        ExtendedRetrieverSpanRecord,
                    ),
                ):
                    records_item = records_item_data.to_dict()
                else:
                    records_item = records_item_data.to_dict()

                records.append(records_item)

        starting_token = self.starting_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limit is not UNSET:
            field_dict["limit"] = limit
        if next_starting_token is not UNSET:
            field_dict["next_starting_token"] = next_starting_token
        if paginated is not UNSET:
            field_dict["paginated"] = paginated
        if records is not UNSET:
            field_dict["records"] = records
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.extended_agent_span_record import ExtendedAgentSpanRecord
        from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
        from ..models.extended_retriever_span_record import ExtendedRetrieverSpanRecord
        from ..models.extended_session_record import ExtendedSessionRecord
        from ..models.extended_tool_span_record import ExtendedToolSpanRecord
        from ..models.extended_trace_record import ExtendedTraceRecord
        from ..models.extended_workflow_span_record import ExtendedWorkflowSpanRecord

        d = dict(src_dict)
        limit = d.pop("limit", UNSET)

        def _parse_next_starting_token(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        next_starting_token = _parse_next_starting_token(d.pop("next_starting_token", UNSET))

        paginated = d.pop("paginated", UNSET)

        records = []
        _records = d.pop("records", UNSET)
        for records_item_data in _records or []:

            def _parse_records_item(
                data: object,
            ) -> Union[
                "ExtendedAgentSpanRecord",
                "ExtendedLlmSpanRecord",
                "ExtendedRetrieverSpanRecord",
                "ExtendedSessionRecord",
                "ExtendedToolSpanRecord",
                "ExtendedTraceRecord",
                "ExtendedWorkflowSpanRecord",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedTraceRecord.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedAgentSpanRecord.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedWorkflowSpanRecord.from_dict(data)

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
                    return ExtendedToolSpanRecord.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedRetrieverSpanRecord.from_dict(data)

                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                return ExtendedSessionRecord.from_dict(data)

            records_item = _parse_records_item(records_item_data)

            records.append(records_item)

        starting_token = d.pop("starting_token", UNSET)

        log_records_query_response = cls(
            limit=limit,
            next_starting_token=next_starting_token,
            paginated=paginated,
            records=records,
            starting_token=starting_token,
        )

        log_records_query_response.additional_properties = d
        return log_records_query_response

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
