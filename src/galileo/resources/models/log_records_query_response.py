from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.llm_span_record import LlmSpanRecord
    from ..models.retriever_span_record import RetrieverSpanRecord
    from ..models.tool_span_record import ToolSpanRecord
    from ..models.trace_record import TraceRecord
    from ..models.workflow_span_record import WorkflowSpanRecord


T = TypeVar("T", bound="LogRecordsQueryResponse")


@_attrs_define
class LogRecordsQueryResponse:
    """
    Attributes:
        limit (Union[Unset, int]):  Default: 100.
        next_starting_token (Union[None, Unset, int]):
        paginated (Union[Unset, bool]):  Default: False.
        records (Union[Unset, list[Union['LlmSpanRecord', 'RetrieverSpanRecord', 'ToolSpanRecord', 'TraceRecord',
            'WorkflowSpanRecord']]]): records matching the query
        starting_token (Union[Unset, int]):  Default: 0.
    """

    limit: Union[Unset, int] = 100
    next_starting_token: Union[None, Unset, int] = UNSET
    paginated: Union[Unset, bool] = False
    records: Union[
        Unset,
        list[Union["LlmSpanRecord", "RetrieverSpanRecord", "ToolSpanRecord", "TraceRecord", "WorkflowSpanRecord"]],
    ] = UNSET
    starting_token: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.llm_span_record import LlmSpanRecord
        from ..models.tool_span_record import ToolSpanRecord
        from ..models.trace_record import TraceRecord
        from ..models.workflow_span_record import WorkflowSpanRecord

        limit = self.limit

        next_starting_token: Union[None, Unset, int]
        if isinstance(self.next_starting_token, Unset):
            next_starting_token = UNSET
        else:
            next_starting_token = self.next_starting_token

        paginated = self.paginated

        records: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.records, Unset):
            records = []
            for records_item_data in self.records:
                records_item: dict[str, Any]
                if isinstance(records_item_data, TraceRecord):
                    records_item = records_item_data.to_dict()
                elif isinstance(records_item_data, WorkflowSpanRecord):
                    records_item = records_item_data.to_dict()
                elif isinstance(records_item_data, LlmSpanRecord):
                    records_item = records_item_data.to_dict()
                elif isinstance(records_item_data, ToolSpanRecord):
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.llm_span_record import LlmSpanRecord
        from ..models.retriever_span_record import RetrieverSpanRecord
        from ..models.tool_span_record import ToolSpanRecord
        from ..models.trace_record import TraceRecord
        from ..models.workflow_span_record import WorkflowSpanRecord

        d = src_dict.copy()
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
            ) -> Union["LlmSpanRecord", "RetrieverSpanRecord", "ToolSpanRecord", "TraceRecord", "WorkflowSpanRecord"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    records_item_type_0 = TraceRecord.from_dict(data)

                    return records_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    records_item_type_1_type_0 = WorkflowSpanRecord.from_dict(data)

                    return records_item_type_1_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    records_item_type_1_type_1 = LlmSpanRecord.from_dict(data)

                    return records_item_type_1_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    records_item_type_1_type_2 = ToolSpanRecord.from_dict(data)

                    return records_item_type_1_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                records_item_type_1_type_3 = RetrieverSpanRecord.from_dict(data)

                return records_item_type_1_type_3

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
