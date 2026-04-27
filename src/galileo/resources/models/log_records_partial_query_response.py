from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.partial_extended_agent_span_record import PartialExtendedAgentSpanRecord
    from ..models.partial_extended_control_span_record import PartialExtendedControlSpanRecord
    from ..models.partial_extended_llm_span_record import PartialExtendedLlmSpanRecord
    from ..models.partial_extended_retriever_span_record import PartialExtendedRetrieverSpanRecord
    from ..models.partial_extended_session_record import PartialExtendedSessionRecord
    from ..models.partial_extended_tool_span_record import PartialExtendedToolSpanRecord
    from ..models.partial_extended_trace_record import PartialExtendedTraceRecord
    from ..models.partial_extended_workflow_span_record import PartialExtendedWorkflowSpanRecord


T = TypeVar("T", bound="LogRecordsPartialQueryResponse")


@_attrs_define
class LogRecordsPartialQueryResponse:
    """
    Attributes:
        num_records (int): number of records
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.
        paginated (bool | Unset):  Default: False.
        next_starting_token (int | None | Unset):
        last_row_id (None | str | Unset):
        records (list[PartialExtendedAgentSpanRecord | PartialExtendedControlSpanRecord | PartialExtendedLlmSpanRecord |
            PartialExtendedRetrieverSpanRecord | PartialExtendedSessionRecord | PartialExtendedToolSpanRecord |
            PartialExtendedTraceRecord | PartialExtendedWorkflowSpanRecord] | Unset): records matching the query
    """

    num_records: int
    starting_token: int | Unset = 0
    limit: int | Unset = 100
    paginated: bool | Unset = False
    next_starting_token: int | None | Unset = UNSET
    last_row_id: None | str | Unset = UNSET
    records: (
        list[
            PartialExtendedAgentSpanRecord
            | PartialExtendedControlSpanRecord
            | PartialExtendedLlmSpanRecord
            | PartialExtendedRetrieverSpanRecord
            | PartialExtendedSessionRecord
            | PartialExtendedToolSpanRecord
            | PartialExtendedTraceRecord
            | PartialExtendedWorkflowSpanRecord
        ]
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.partial_extended_agent_span_record import PartialExtendedAgentSpanRecord
        from ..models.partial_extended_control_span_record import PartialExtendedControlSpanRecord
        from ..models.partial_extended_llm_span_record import PartialExtendedLlmSpanRecord
        from ..models.partial_extended_retriever_span_record import PartialExtendedRetrieverSpanRecord
        from ..models.partial_extended_tool_span_record import PartialExtendedToolSpanRecord
        from ..models.partial_extended_trace_record import PartialExtendedTraceRecord
        from ..models.partial_extended_workflow_span_record import PartialExtendedWorkflowSpanRecord

        num_records = self.num_records

        starting_token = self.starting_token

        limit = self.limit

        paginated = self.paginated

        next_starting_token: int | None | Unset
        if isinstance(self.next_starting_token, Unset):
            next_starting_token = UNSET
        else:
            next_starting_token = self.next_starting_token

        last_row_id: None | str | Unset
        if isinstance(self.last_row_id, Unset):
            last_row_id = UNSET
        else:
            last_row_id = self.last_row_id

        records: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.records, Unset):
            records = []
            for records_item_data in self.records:
                records_item: dict[str, Any]
                if isinstance(records_item_data, PartialExtendedTraceRecord):
                    records_item = records_item_data.to_dict()
                elif isinstance(records_item_data, PartialExtendedAgentSpanRecord):
                    records_item = records_item_data.to_dict()
                elif isinstance(records_item_data, PartialExtendedWorkflowSpanRecord):
                    records_item = records_item_data.to_dict()
                elif isinstance(records_item_data, PartialExtendedLlmSpanRecord):
                    records_item = records_item_data.to_dict()
                elif isinstance(records_item_data, PartialExtendedToolSpanRecord):
                    records_item = records_item_data.to_dict()
                elif isinstance(records_item_data, PartialExtendedRetrieverSpanRecord):
                    records_item = records_item_data.to_dict()
                elif isinstance(records_item_data, PartialExtendedControlSpanRecord):
                    records_item = records_item_data.to_dict()
                else:
                    records_item = records_item_data.to_dict()

                records.append(records_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"num_records": num_records})
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
        from ..models.partial_extended_agent_span_record import PartialExtendedAgentSpanRecord
        from ..models.partial_extended_control_span_record import PartialExtendedControlSpanRecord
        from ..models.partial_extended_llm_span_record import PartialExtendedLlmSpanRecord
        from ..models.partial_extended_retriever_span_record import PartialExtendedRetrieverSpanRecord
        from ..models.partial_extended_session_record import PartialExtendedSessionRecord
        from ..models.partial_extended_tool_span_record import PartialExtendedToolSpanRecord
        from ..models.partial_extended_trace_record import PartialExtendedTraceRecord
        from ..models.partial_extended_workflow_span_record import PartialExtendedWorkflowSpanRecord

        d = dict(src_dict)
        num_records = d.pop("num_records")

        starting_token = d.pop("starting_token", UNSET)

        limit = d.pop("limit", UNSET)

        paginated = d.pop("paginated", UNSET)

        def _parse_next_starting_token(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        next_starting_token = _parse_next_starting_token(d.pop("next_starting_token", UNSET))

        def _parse_last_row_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_row_id = _parse_last_row_id(d.pop("last_row_id", UNSET))

        _records = d.pop("records", UNSET)
        records: (
            list[
                PartialExtendedAgentSpanRecord
                | PartialExtendedControlSpanRecord
                | PartialExtendedLlmSpanRecord
                | PartialExtendedRetrieverSpanRecord
                | PartialExtendedSessionRecord
                | PartialExtendedToolSpanRecord
                | PartialExtendedTraceRecord
                | PartialExtendedWorkflowSpanRecord
            ]
            | Unset
        ) = UNSET
        if _records is not UNSET:
            records = []
            for records_item_data in _records:

                def _parse_records_item(
                    data: object,
                ) -> (
                    PartialExtendedAgentSpanRecord
                    | PartialExtendedControlSpanRecord
                    | PartialExtendedLlmSpanRecord
                    | PartialExtendedRetrieverSpanRecord
                    | PartialExtendedSessionRecord
                    | PartialExtendedToolSpanRecord
                    | PartialExtendedTraceRecord
                    | PartialExtendedWorkflowSpanRecord
                ):
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
                        records_item_type_0 = PartialExtendedTraceRecord.from_dict(data)

                        return records_item_type_0
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        records_item_type_1 = PartialExtendedAgentSpanRecord.from_dict(data)

                        return records_item_type_1
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        records_item_type_2 = PartialExtendedWorkflowSpanRecord.from_dict(data)

                        return records_item_type_2
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        records_item_type_3 = PartialExtendedLlmSpanRecord.from_dict(data)

                        return records_item_type_3
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        records_item_type_4 = PartialExtendedToolSpanRecord.from_dict(data)

                        return records_item_type_4
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        records_item_type_5 = PartialExtendedRetrieverSpanRecord.from_dict(data)

                        return records_item_type_5
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        records_item_type_6 = PartialExtendedControlSpanRecord.from_dict(data)

                        return records_item_type_6
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        records_item_type_7 = PartialExtendedSessionRecord.from_dict(data)

                        return records_item_type_7
                    except:  # noqa: E722
                        pass
                    # If we reach here, none of the parsers succeeded
                    discriminator_info = (
                        f" (type={data.get('type')})" if isinstance(data, dict) and "type" in data else ""
                    )
                    raise ValueError(f"Could not parse union type for records_item{discriminator_info}")

                records_item = _parse_records_item(records_item_data)

                records.append(records_item)

        log_records_partial_query_response = cls(
            num_records=num_records,
            starting_token=starting_token,
            limit=limit,
            paginated=paginated,
            next_starting_token=next_starting_token,
            last_row_id=last_row_id,
            records=records,
        )

        log_records_partial_query_response.additional_properties = d
        return log_records_partial_query_response

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
