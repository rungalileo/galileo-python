from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_status import ExecutionStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.action_result import ActionResult
    from ..models.invoke_response_headers_type_0 import InvokeResponseHeadersType0
    from ..models.invoke_response_metadata_type_0 import InvokeResponseMetadataType0
    from ..models.invoke_response_metric_results import InvokeResponseMetricResults
    from ..models.ruleset_result import RulesetResult
    from ..models.stage_metadata import StageMetadata
    from ..models.trace_metadata import TraceMetadata


T = TypeVar("T", bound="InvokeResponse")


@_attrs_define
class InvokeResponse:
    """
    Attributes:
        action_result (ActionResult):
        stage_metadata (StageMetadata):
        text (str): Text from the request after processing the rules.
        trace_metadata (TraceMetadata):
        api_version (Union[Unset, str]):  Default: '1.0.0'.
        headers (Union['InvokeResponseHeadersType0', None, Unset]): Optional additional HTTP headers that should be
            included in the response.
        metadata (Union['InvokeResponseMetadataType0', None, Unset]): Optional additional metadata. This being echoed
            back from the request.
        metric_results (Union[Unset, InvokeResponseMetricResults]): Results of the metric computation.
        ruleset_results (Union[Unset, list['RulesetResult']]): Results of the rule execution.
        status (Union[Unset, ExecutionStatus]): Status of the execution.
    """

    action_result: "ActionResult"
    stage_metadata: "StageMetadata"
    text: str
    trace_metadata: "TraceMetadata"
    api_version: Union[Unset, str] = "1.0.0"
    headers: Union["InvokeResponseHeadersType0", None, Unset] = UNSET
    metadata: Union["InvokeResponseMetadataType0", None, Unset] = UNSET
    metric_results: Union[Unset, "InvokeResponseMetricResults"] = UNSET
    ruleset_results: Union[Unset, list["RulesetResult"]] = UNSET
    status: Union[Unset, ExecutionStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.invoke_response_headers_type_0 import InvokeResponseHeadersType0
        from ..models.invoke_response_metadata_type_0 import InvokeResponseMetadataType0

        action_result = self.action_result.to_dict()

        stage_metadata = self.stage_metadata.to_dict()

        text = self.text

        trace_metadata = self.trace_metadata.to_dict()

        api_version = self.api_version

        headers: Union[None, Unset, dict[str, Any]]
        if isinstance(self.headers, Unset):
            headers = UNSET
        elif isinstance(self.headers, InvokeResponseHeadersType0):
            headers = self.headers.to_dict()
        else:
            headers = self.headers

        metadata: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, InvokeResponseMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        metric_results: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metric_results, Unset):
            metric_results = self.metric_results.to_dict()

        ruleset_results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ruleset_results, Unset):
            ruleset_results = []
            for ruleset_results_item_data in self.ruleset_results:
                ruleset_results_item = ruleset_results_item_data.to_dict()
                ruleset_results.append(ruleset_results_item)

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action_result": action_result,
                "stage_metadata": stage_metadata,
                "text": text,
                "trace_metadata": trace_metadata,
            }
        )
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if headers is not UNSET:
            field_dict["headers"] = headers
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if metric_results is not UNSET:
            field_dict["metric_results"] = metric_results
        if ruleset_results is not UNSET:
            field_dict["ruleset_results"] = ruleset_results
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.action_result import ActionResult
        from ..models.invoke_response_headers_type_0 import InvokeResponseHeadersType0
        from ..models.invoke_response_metadata_type_0 import InvokeResponseMetadataType0
        from ..models.invoke_response_metric_results import InvokeResponseMetricResults
        from ..models.ruleset_result import RulesetResult
        from ..models.stage_metadata import StageMetadata
        from ..models.trace_metadata import TraceMetadata

        d = src_dict.copy()
        action_result = ActionResult.from_dict(d.pop("action_result"))

        stage_metadata = StageMetadata.from_dict(d.pop("stage_metadata"))

        text = d.pop("text")

        trace_metadata = TraceMetadata.from_dict(d.pop("trace_metadata"))

        api_version = d.pop("api_version", UNSET)

        def _parse_headers(data: object) -> Union["InvokeResponseHeadersType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                headers_type_0 = InvokeResponseHeadersType0.from_dict(data)

                return headers_type_0
            except:  # noqa: E722
                pass
            return cast(Union["InvokeResponseHeadersType0", None, Unset], data)

        headers = _parse_headers(d.pop("headers", UNSET))

        def _parse_metadata(data: object) -> Union["InvokeResponseMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = InvokeResponseMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["InvokeResponseMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        _metric_results = d.pop("metric_results", UNSET)
        metric_results: Union[Unset, InvokeResponseMetricResults]
        if isinstance(_metric_results, Unset):
            metric_results = UNSET
        else:
            metric_results = InvokeResponseMetricResults.from_dict(_metric_results)

        ruleset_results = []
        _ruleset_results = d.pop("ruleset_results", UNSET)
        for ruleset_results_item_data in _ruleset_results or []:
            ruleset_results_item = RulesetResult.from_dict(ruleset_results_item_data)

            ruleset_results.append(ruleset_results_item)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ExecutionStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ExecutionStatus(_status)

        invoke_response = cls(
            action_result=action_result,
            stage_metadata=stage_metadata,
            text=text,
            trace_metadata=trace_metadata,
            api_version=api_version,
            headers=headers,
            metadata=metadata,
            metric_results=metric_results,
            ruleset_results=ruleset_results,
            status=status,
        )

        invoke_response.additional_properties = d
        return invoke_response

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
