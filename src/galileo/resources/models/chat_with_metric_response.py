from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_metric_suggestion_label import AutoMetricSuggestionLabel
from ..models.job_status import JobStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChatWithMetricResponse")


@_attrs_define
class ChatWithMetricResponse:
    """
    Attributes:
        project_id (str):
        log_stream_id (str):
        chat_query (str):
        metric_name (str):
        label (AutoMetricSuggestionLabel | None | Unset):
        description (None | str | Unset):
        chat_response (None | str | Unset):
        job_status (JobStatus | None | Unset):
    """

    project_id: str
    log_stream_id: str
    chat_query: str
    metric_name: str
    label: AutoMetricSuggestionLabel | None | Unset = UNSET
    description: None | str | Unset = UNSET
    chat_response: None | str | Unset = UNSET
    job_status: JobStatus | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        log_stream_id = self.log_stream_id

        chat_query = self.chat_query

        metric_name = self.metric_name

        label: None | str | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        elif isinstance(self.label, AutoMetricSuggestionLabel):
            label = self.label.value
        else:
            label = self.label

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        chat_response: None | str | Unset
        if isinstance(self.chat_response, Unset):
            chat_response = UNSET
        else:
            chat_response = self.chat_response

        job_status: None | str | Unset
        if isinstance(self.job_status, Unset):
            job_status = UNSET
        elif isinstance(self.job_status, JobStatus):
            job_status = self.job_status.value
        else:
            job_status = self.job_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "log_stream_id": log_stream_id,
                "chat_query": chat_query,
                "metric_name": metric_name,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if description is not UNSET:
            field_dict["description"] = description
        if chat_response is not UNSET:
            field_dict["chat_response"] = chat_response
        if job_status is not UNSET:
            field_dict["job_status"] = job_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        log_stream_id = d.pop("log_stream_id")

        chat_query = d.pop("chat_query")

        metric_name = d.pop("metric_name")

        def _parse_label(data: object) -> AutoMetricSuggestionLabel | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                label_type_0 = AutoMetricSuggestionLabel(data)

                return label_type_0
            except:  # noqa: E722
                pass
            return cast(AutoMetricSuggestionLabel | None | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_chat_response(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        chat_response = _parse_chat_response(d.pop("chat_response", UNSET))

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

        chat_with_metric_response = cls(
            project_id=project_id,
            log_stream_id=log_stream_id,
            chat_query=chat_query,
            metric_name=metric_name,
            label=label,
            description=description,
            chat_response=chat_response,
            job_status=job_status,
        )

        chat_with_metric_response.additional_properties = d
        return chat_with_metric_response

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
