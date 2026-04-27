from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..models.scorer_type import ScorerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="JobInfo")


@_attrs_define
class JobInfo:
    """
    Attributes:
        job_status (JobStatus | None | Unset): Job status used for computing the column. Only set for metrics columns
            that have a separate scorer job.
        job_progress_message (None | str | Unset): Progress message to show the users on hover in case the job is in
            progress.
        job_error_message (None | str | Unset): Error message to show the users on hover in case the job fails or errors
            out.
        scorer_name (None | str | Unset): Scorer Name executed by the job.
        job_type (None | ScorerType | Unset): Whether a job is designated as plus or basic.
    """

    job_status: JobStatus | None | Unset = UNSET
    job_progress_message: None | str | Unset = UNSET
    job_error_message: None | str | Unset = UNSET
    scorer_name: None | str | Unset = UNSET
    job_type: None | ScorerType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_status: None | str | Unset
        if isinstance(self.job_status, Unset):
            job_status = UNSET
        elif isinstance(self.job_status, JobStatus):
            job_status = self.job_status.value
        else:
            job_status = self.job_status

        job_progress_message: None | str | Unset
        if isinstance(self.job_progress_message, Unset):
            job_progress_message = UNSET
        else:
            job_progress_message = self.job_progress_message

        job_error_message: None | str | Unset
        if isinstance(self.job_error_message, Unset):
            job_error_message = UNSET
        else:
            job_error_message = self.job_error_message

        scorer_name: None | str | Unset
        if isinstance(self.scorer_name, Unset):
            scorer_name = UNSET
        else:
            scorer_name = self.scorer_name

        job_type: None | str | Unset
        if isinstance(self.job_type, Unset):
            job_type = UNSET
        elif isinstance(self.job_type, ScorerType):
            job_type = self.job_type.value
        else:
            job_type = self.job_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_status is not UNSET:
            field_dict["job_status"] = job_status
        if job_progress_message is not UNSET:
            field_dict["job_progress_message"] = job_progress_message
        if job_error_message is not UNSET:
            field_dict["job_error_message"] = job_error_message
        if scorer_name is not UNSET:
            field_dict["scorer_name"] = scorer_name
        if job_type is not UNSET:
            field_dict["job_type"] = job_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

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

        def _parse_job_progress_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        job_progress_message = _parse_job_progress_message(d.pop("job_progress_message", UNSET))

        def _parse_job_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        job_error_message = _parse_job_error_message(d.pop("job_error_message", UNSET))

        def _parse_scorer_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        scorer_name = _parse_scorer_name(d.pop("scorer_name", UNSET))

        def _parse_job_type(data: object) -> None | ScorerType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_type_type_0 = ScorerType(data)

                return job_type_type_0
            except:  # noqa: E722
                pass
            return cast(None | ScorerType | Unset, data)

        job_type = _parse_job_type(d.pop("job_type", UNSET))

        job_info = cls(
            job_status=job_status,
            job_progress_message=job_progress_message,
            job_error_message=job_error_message,
            scorer_name=scorer_name,
            job_type=job_type,
        )

        job_info.additional_properties = d
        return job_info

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
