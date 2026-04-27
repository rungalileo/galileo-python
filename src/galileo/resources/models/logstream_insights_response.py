from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_status import JobStatus

if TYPE_CHECKING:
    from ..models.insight_db import InsightDB
    from ..models.insight_dbv2 import InsightDBV2


T = TypeVar("T", bound="LogstreamInsightsResponse")


@_attrs_define
class LogstreamInsightsResponse:
    """
    Attributes:
        insights (list[InsightDB] | list[InsightDBV2] | None):
        job_status (JobStatus | None):
        is_update_job (bool):
        job_updated_at (datetime.datetime | None):
    """

    insights: list[InsightDB] | list[InsightDBV2] | None
    job_status: JobStatus | None
    is_update_job: bool
    job_updated_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        insights: list[dict[str, Any]] | None
        if isinstance(self.insights, list):
            insights = []
            for insights_type_0_item_data in self.insights:
                insights_type_0_item = insights_type_0_item_data.to_dict()
                insights.append(insights_type_0_item)

        elif isinstance(self.insights, list):
            insights = []
            for insights_type_1_item_data in self.insights:
                insights_type_1_item = insights_type_1_item_data.to_dict()
                insights.append(insights_type_1_item)

        else:
            insights = self.insights

        job_status: None | str
        if isinstance(self.job_status, JobStatus):
            job_status = self.job_status.value
        else:
            job_status = self.job_status

        is_update_job = self.is_update_job

        job_updated_at: None | str
        if isinstance(self.job_updated_at, datetime.datetime):
            job_updated_at = self.job_updated_at.isoformat()
        else:
            job_updated_at = self.job_updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "insights": insights,
                "job_status": job_status,
                "is_update_job": is_update_job,
                "job_updated_at": job_updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.insight_db import InsightDB
        from ..models.insight_dbv2 import InsightDBV2

        d = dict(src_dict)

        def _parse_insights(data: object) -> list[InsightDB] | list[InsightDBV2] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                insights_type_0 = []
                _insights_type_0 = data
                for insights_type_0_item_data in _insights_type_0:
                    insights_type_0_item = InsightDBV2.from_dict(insights_type_0_item_data)

                    insights_type_0.append(insights_type_0_item)

                return insights_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                insights_type_1 = []
                _insights_type_1 = data
                for insights_type_1_item_data in _insights_type_1:
                    insights_type_1_item = InsightDB.from_dict(insights_type_1_item_data)

                    insights_type_1.append(insights_type_1_item)

                return insights_type_1
            except:  # noqa: E722
                pass
            return cast(list[InsightDB] | list[InsightDBV2] | None, data)

        insights = _parse_insights(d.pop("insights"))

        def _parse_job_status(data: object) -> JobStatus | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_status_type_0 = JobStatus(data)

                return job_status_type_0
            except:  # noqa: E722
                pass
            return cast(JobStatus | None, data)

        job_status = _parse_job_status(d.pop("job_status"))

        is_update_job = d.pop("is_update_job")

        def _parse_job_updated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_updated_at_type_0 = isoparse(data)

                return job_updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(datetime.datetime | None, data)

        job_updated_at = _parse_job_updated_at(d.pop("job_updated_at"))

        logstream_insights_response = cls(
            insights=insights, job_status=job_status, is_update_job=is_update_job, job_updated_at=job_updated_at
        )

        logstream_insights_response.additional_properties = d
        return logstream_insights_response

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
