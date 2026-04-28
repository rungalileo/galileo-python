from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

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
    Attributes
    ----------
        text (str): Text from the request after processing the rules.
        trace_metadata (TraceMetadata):
        stage_metadata (StageMetadata):
        action_result (ActionResult):
        status (ExecutionStatus | Unset): Status of the execution.
        api_version (str | Unset):  Default: '1.0.0'.
        ruleset_results (list[RulesetResult] | Unset): Results of the rule execution.
        metric_results (InvokeResponseMetricResults | Unset): Results of the metric computation.
        metadata (InvokeResponseMetadataType0 | None | Unset): Optional additional metadata. This being echoed back from
            the request.
        headers (InvokeResponseHeadersType0 | None | Unset): Optional additional HTTP headers that should be included in
            the response.
    """

    text: str
    trace_metadata: TraceMetadata
    stage_metadata: StageMetadata
    action_result: ActionResult
    status: ExecutionStatus | Unset = UNSET
    api_version: str | Unset = "1.0.0"
    ruleset_results: list[RulesetResult] | Unset = UNSET
    metric_results: InvokeResponseMetricResults | Unset = UNSET
    metadata: InvokeResponseMetadataType0 | None | Unset = UNSET
    headers: InvokeResponseHeadersType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.invoke_response_headers_type_0 import InvokeResponseHeadersType0
        from ..models.invoke_response_metadata_type_0 import InvokeResponseMetadataType0

        text = self.text

        trace_metadata = self.trace_metadata.to_dict()

        stage_metadata = self.stage_metadata.to_dict()

        action_result = self.action_result.to_dict()

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        api_version = self.api_version

        ruleset_results: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ruleset_results, Unset):
            ruleset_results = []
            for ruleset_results_item_data in self.ruleset_results:
                ruleset_results_item = ruleset_results_item_data.to_dict()
                ruleset_results.append(ruleset_results_item)

        metric_results: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metric_results, Unset):
            metric_results = self.metric_results.to_dict()

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, InvokeResponseMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        headers: dict[str, Any] | None | Unset
        if isinstance(self.headers, Unset):
            headers = UNSET
        elif isinstance(self.headers, InvokeResponseHeadersType0):
            headers = self.headers.to_dict()
        else:
            headers = self.headers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
                "trace_metadata": trace_metadata,
                "stage_metadata": stage_metadata,
                "action_result": action_result,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if ruleset_results is not UNSET:
            field_dict["ruleset_results"] = ruleset_results
        if metric_results is not UNSET:
            field_dict["metric_results"] = metric_results
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if headers is not UNSET:
            field_dict["headers"] = headers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.action_result import ActionResult
        from ..models.invoke_response_headers_type_0 import InvokeResponseHeadersType0
        from ..models.invoke_response_metadata_type_0 import InvokeResponseMetadataType0
        from ..models.invoke_response_metric_results import InvokeResponseMetricResults
        from ..models.ruleset_result import RulesetResult
        from ..models.stage_metadata import StageMetadata
        from ..models.trace_metadata import TraceMetadata

        d = dict(src_dict)
        text = d.pop("text")

        trace_metadata = TraceMetadata.from_dict(d.pop("trace_metadata"))

        stage_metadata = StageMetadata.from_dict(d.pop("stage_metadata"))

        action_result = ActionResult.from_dict(d.pop("action_result"))

        _status = d.pop("status", UNSET)
        status: ExecutionStatus | Unset
        status = UNSET if isinstance(_status, Unset) else ExecutionStatus(_status)

        api_version = d.pop("api_version", UNSET)

        _ruleset_results = d.pop("ruleset_results", UNSET)
        ruleset_results: list[RulesetResult] | Unset = UNSET
        if _ruleset_results is not UNSET:
            ruleset_results = []
            for ruleset_results_item_data in _ruleset_results:
                ruleset_results_item = RulesetResult.from_dict(ruleset_results_item_data)

                ruleset_results.append(ruleset_results_item)

        _metric_results = d.pop("metric_results", UNSET)
        metric_results: InvokeResponseMetricResults | Unset
        if isinstance(_metric_results, Unset):
            metric_results = UNSET
        else:
            metric_results = InvokeResponseMetricResults.from_dict(_metric_results)

        def _parse_metadata(data: object) -> InvokeResponseMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return InvokeResponseMetadataType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(InvokeResponseMetadataType0 | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_headers(data: object) -> InvokeResponseHeadersType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return InvokeResponseHeadersType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(InvokeResponseHeadersType0 | None | Unset, data)

        headers = _parse_headers(d.pop("headers", UNSET))

        invoke_response = cls(
            text=text,
            trace_metadata=trace_metadata,
            stage_metadata=stage_metadata,
            action_result=action_result,
            status=status,
            api_version=api_version,
            ruleset_results=ruleset_results,
            metric_results=metric_results,
            metadata=metadata,
            headers=headers,
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
