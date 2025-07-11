from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.logging_method import LoggingMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_span import AgentSpan
    from ..models.llm_span import LlmSpan
    from ..models.retriever_span import RetrieverSpan
    from ..models.tool_span import ToolSpan
    from ..models.workflow_span import WorkflowSpan


T = TypeVar("T", bound="LogSpansIngestRequest")


@_attrs_define
class LogSpansIngestRequest:
    """Request model for ingesting spans.

    Attributes:
        parent_id (str): Parent trace or span id.
        spans (list[Union['AgentSpan', 'LlmSpan', 'RetrieverSpan', 'ToolSpan', 'WorkflowSpan']]): List of spans to log.
        trace_id (str): Trace id associated with the spans.
        client_version (Union[None, Unset, str]):
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        logging_method (Union[Unset, LoggingMethod]):
        reliable (Union[Unset, bool]): Whether or not to use reliable logging.  If set to False, the method will respond
            immediately before verifying that the traces have been successfully ingested, and no error message will be
            returned if ingestion fails.  If set to True, the method will wait for the traces to be successfully ingested or
            return an error message if there is an ingestion failure. Default: False.
    """

    parent_id: str
    spans: list[Union["AgentSpan", "LlmSpan", "RetrieverSpan", "ToolSpan", "WorkflowSpan"]]
    trace_id: str
    client_version: Union[None, Unset, str] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    log_stream_id: Union[None, Unset, str] = UNSET
    logging_method: Union[Unset, LoggingMethod] = UNSET
    reliable: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_span import AgentSpan
        from ..models.llm_span import LlmSpan
        from ..models.retriever_span import RetrieverSpan
        from ..models.workflow_span import WorkflowSpan

        parent_id = self.parent_id

        spans = []
        for spans_item_data in self.spans:
            spans_item: dict[str, Any]
            if isinstance(spans_item_data, AgentSpan):
                spans_item = spans_item_data.to_dict()
            elif isinstance(spans_item_data, WorkflowSpan):
                spans_item = spans_item_data.to_dict()
            elif isinstance(spans_item_data, LlmSpan):
                spans_item = spans_item_data.to_dict()
            elif isinstance(spans_item_data, RetrieverSpan):
                spans_item = spans_item_data.to_dict()
            else:
                spans_item = spans_item_data.to_dict()

            spans.append(spans_item)

        trace_id = self.trace_id

        client_version: Union[None, Unset, str]
        if isinstance(self.client_version, Unset):
            client_version = UNSET
        else:
            client_version = self.client_version

        experiment_id: Union[None, Unset, str]
        if isinstance(self.experiment_id, Unset):
            experiment_id = UNSET
        else:
            experiment_id = self.experiment_id

        log_stream_id: Union[None, Unset, str]
        if isinstance(self.log_stream_id, Unset):
            log_stream_id = UNSET
        else:
            log_stream_id = self.log_stream_id

        logging_method: Union[Unset, str] = UNSET
        if not isinstance(self.logging_method, Unset):
            logging_method = self.logging_method.value

        reliable = self.reliable

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"parent_id": parent_id, "spans": spans, "trace_id": trace_id})
        if client_version is not UNSET:
            field_dict["client_version"] = client_version
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if logging_method is not UNSET:
            field_dict["logging_method"] = logging_method
        if reliable is not UNSET:
            field_dict["reliable"] = reliable

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_span import AgentSpan
        from ..models.llm_span import LlmSpan
        from ..models.retriever_span import RetrieverSpan
        from ..models.tool_span import ToolSpan
        from ..models.workflow_span import WorkflowSpan

        d = dict(src_dict)
        parent_id = d.pop("parent_id")

        spans = []
        _spans = d.pop("spans")
        for spans_item_data in _spans:

            def _parse_spans_item(
                data: object,
            ) -> Union["AgentSpan", "LlmSpan", "RetrieverSpan", "ToolSpan", "WorkflowSpan"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_0 = AgentSpan.from_dict(data)

                    return spans_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_1 = WorkflowSpan.from_dict(data)

                    return spans_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_2 = LlmSpan.from_dict(data)

                    return spans_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    spans_item_type_3 = RetrieverSpan.from_dict(data)

                    return spans_item_type_3
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                spans_item_type_4 = ToolSpan.from_dict(data)

                return spans_item_type_4

            spans_item = _parse_spans_item(spans_item_data)

            spans.append(spans_item)

        trace_id = d.pop("trace_id")

        def _parse_client_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        client_version = _parse_client_version(d.pop("client_version", UNSET))

        def _parse_experiment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        _logging_method = d.pop("logging_method", UNSET)
        logging_method: Union[Unset, LoggingMethod]
        if isinstance(_logging_method, Unset):
            logging_method = UNSET
        else:
            logging_method = LoggingMethod(_logging_method)

        reliable = d.pop("reliable", UNSET)

        log_spans_ingest_request = cls(
            parent_id=parent_id,
            spans=spans,
            trace_id=trace_id,
            client_version=client_version,
            experiment_id=experiment_id,
            log_stream_id=log_stream_id,
            logging_method=logging_method,
            reliable=reliable,
        )

        log_spans_ingest_request.additional_properties = d
        return log_spans_ingest_request

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
