from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LogstreamInsightsResponseCreateJobResponse")


@_attrs_define
class LogstreamInsightsResponseCreateJobResponse:
    """
    Attributes:
        job_created (bool):
        is_update_job (bool):
    """

    job_created: bool
    is_update_job: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_created = self.job_created

        is_update_job = self.is_update_job

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"job_created": job_created, "is_update_job": is_update_job})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_created = d.pop("job_created")

        is_update_job = d.pop("is_update_job")

        logstream_insights_response_create_job_response = cls(job_created=job_created, is_update_job=is_update_job)

        logstream_insights_response_create_job_response.additional_properties = d
        return logstream_insights_response_create_job_response

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
