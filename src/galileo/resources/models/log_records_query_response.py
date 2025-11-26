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
    Attributes
    ----------
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        paginated (Union[Unset, bool]):  Default: False.
        next_starting_token (Union[None, Unset, int]):
        last_row_id (Union[None, Unset, str]):
        records (Union[Unset, list[Union['ExtendedAgentSpanRecord', 'ExtendedLlmSpanRecord',
            'ExtendedRetrieverSpanRecord', 'ExtendedSessionRecord', 'ExtendedToolSpanRecord', 'ExtendedTraceRecord',
            'ExtendedWorkflowSpanRecord']]]): records matching the query.
    """

    starting_token: Union[Unset, int] = 0
    limit: Union[Unset, int] = 100
    paginated: Union[Unset, bool] = False
    next_starting_token: Union[None, Unset, int] = UNSET
    last_row_id: Union[None, Unset, str] = UNSET
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
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.extended_agent_span_record import ExtendedAgentSpanRecord
        from ..models.extended_llm_span_record import ExtendedLlmSpanRecord
        from ..models.extended_retriever_span_record import ExtendedRetrieverSpanRecord
        from ..models.extended_tool_span_record import ExtendedToolSpanRecord
        from ..models.extended_trace_record import ExtendedTraceRecord
        from ..models.extended_workflow_span_record import ExtendedWorkflowSpanRecord

        starting_token = self.starting_token

        limit = self.limit

        paginated = self.paginated

        next_starting_token: Union[None, Unset, int]
        next_starting_token = UNSET if isinstance(self.next_starting_token, Unset) else self.next_starting_token

        last_row_id: Union[None, Unset, str]
        last_row_id = UNSET if isinstance(self.last_row_id, Unset) else self.last_row_id

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if limit is not UNSET:
            field_dict["limit"] = limit
        if paginated is not UNSET:
            field_dict["paginated"] = paginated
        if next_starting_token is not UNSET:
            field_dict["next_starting_token"] = next_starting_token
        if last_row_id is not UNSET:
            field_dict["last_row_id"] = last_row_id
        if records is not UNSET:
            field_dict["records"] = records

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        starting_token = d.pop("starting_token", UNSET)

        limit = d.pop("limit", UNSET)

        paginated = d.pop("paginated", UNSET)

        def _parse_next_starting_token(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        next_starting_token = _parse_next_starting_token(d.pop("next_starting_token", UNSET))

        def _parse_last_row_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_row_id = _parse_last_row_id(d.pop("last_row_id", UNSET))

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
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return ExtendedSessionRecord.from_dict(data)

                except:  # noqa: E722
                    pass
                # If we reach here, none of the parsers succeeded
                discriminator_info = f" (type={data.get('type')})" if isinstance(data, dict) and "type" in data else ""
                raise ValueError(f"Could not parse union type for records_item{discriminator_info}")

            records_item = _parse_records_item(records_item_data)

            records.append(records_item)

        log_records_query_response = cls(
            starting_token=starting_token,
            limit=limit,
            paginated=paginated,
            next_starting_token=next_starting_token,
            last_row_id=last_row_id,
            records=records,
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
