from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.auto_metric import AutoMetric


T = TypeVar("T", bound="AutoMetricSuggestionGetResponse")


@_attrs_define
class AutoMetricSuggestionGetResponse:
    """
    Attributes:
        project_id (str):
        log_stream_id (str):
        label (None | str | Unset):
        metrics (list[AutoMetric] | None | Unset):
        job_status (JobStatus | None | Unset):
    """

    project_id: str
    log_stream_id: str
    label: None | str | Unset = UNSET
    metrics: list[AutoMetric] | None | Unset = UNSET
    job_status: JobStatus | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        log_stream_id = self.log_stream_id

        label: None | str | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        metrics: list[dict[str, Any]] | None | Unset
        if isinstance(self.metrics, Unset):
            metrics = UNSET
        elif isinstance(self.metrics, list):
            metrics = []
            for metrics_type_0_item_data in self.metrics:
                metrics_type_0_item = metrics_type_0_item_data.to_dict()
                metrics.append(metrics_type_0_item)

        else:
            metrics = self.metrics

        job_status: None | str | Unset
        if isinstance(self.job_status, Unset):
            job_status = UNSET
        elif isinstance(self.job_status, JobStatus):
            job_status = self.job_status.value
        else:
            job_status = self.job_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "log_stream_id": log_stream_id})
        if label is not UNSET:
            field_dict["label"] = label
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if job_status is not UNSET:
            field_dict["job_status"] = job_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auto_metric import AutoMetric

        d = dict(src_dict)
        project_id = d.pop("project_id")

        log_stream_id = d.pop("log_stream_id")

        def _parse_label(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_metrics(data: object) -> list[AutoMetric] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                metrics_type_0 = []
                _metrics_type_0 = data
                for metrics_type_0_item_data in _metrics_type_0:
                    metrics_type_0_item = AutoMetric.from_dict(metrics_type_0_item_data)

                    metrics_type_0.append(metrics_type_0_item)

                return metrics_type_0
            except:  # noqa: E722
                pass
            return cast(list[AutoMetric] | None | Unset, data)

        metrics = _parse_metrics(d.pop("metrics", UNSET))

        def _parse_job_status(data: object) -> JobStatus | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_status_type_0 = JobStatus(data)

                return job_status_type_0
            except:  # noqa: E722
                pass
            return cast(JobStatus | None | Unset, data)

        job_status = _parse_job_status(d.pop("job_status", UNSET))

        auto_metric_suggestion_get_response = cls(
            project_id=project_id, log_stream_id=log_stream_id, label=label, metrics=metrics, job_status=job_status
        )

        auto_metric_suggestion_get_response.additional_properties = d
        return auto_metric_suggestion_get_response

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
