import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_db_request_data import JobDBRequestData


T = TypeVar("T", bound="JobDB")


@_attrs_define
class JobDB:
    """
    Attributes:
        created_at (datetime.datetime):
        id (str):
        job_name (str):
        project_id (str):
        request_data (JobDBRequestData):
        retries (int):
        run_id (str):
        status (str):
        updated_at (datetime.datetime):
        completed_at (Union[None, Unset, datetime.datetime]):
        error_message (Union[None, Unset, str]):
        failed_at (Union[None, Unset, datetime.datetime]):
        migration_name (Union[None, Unset, str]):
        monitor_batch_id (Union[None, Unset, str]):
        processing_started (Union[None, Unset, datetime.datetime]):
        progress_message (Union[None, Unset, str]):
        progress_percent (Union[Unset, float]):  Default: 0.0.
        steps_completed (Union[Unset, int]):  Default: 0.
        steps_total (Union[Unset, int]):  Default: 0.
    """

    created_at: datetime.datetime
    id: str
    job_name: str
    project_id: str
    request_data: "JobDBRequestData"
    retries: int
    run_id: str
    status: str
    updated_at: datetime.datetime
    completed_at: Union[None, Unset, datetime.datetime] = UNSET
    error_message: Union[None, Unset, str] = UNSET
    failed_at: Union[None, Unset, datetime.datetime] = UNSET
    migration_name: Union[None, Unset, str] = UNSET
    monitor_batch_id: Union[None, Unset, str] = UNSET
    processing_started: Union[None, Unset, datetime.datetime] = UNSET
    progress_message: Union[None, Unset, str] = UNSET
    progress_percent: Union[Unset, float] = 0.0
    steps_completed: Union[Unset, int] = 0
    steps_total: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        job_name = self.job_name

        project_id = self.project_id

        request_data = self.request_data.to_dict()

        retries = self.retries

        run_id = self.run_id

        status = self.status

        updated_at = self.updated_at.isoformat()

        completed_at: Union[None, Unset, str]
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        error_message: Union[None, Unset, str]
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        failed_at: Union[None, Unset, str]
        if isinstance(self.failed_at, Unset):
            failed_at = UNSET
        elif isinstance(self.failed_at, datetime.datetime):
            failed_at = self.failed_at.isoformat()
        else:
            failed_at = self.failed_at

        migration_name: Union[None, Unset, str]
        if isinstance(self.migration_name, Unset):
            migration_name = UNSET
        else:
            migration_name = self.migration_name

        monitor_batch_id: Union[None, Unset, str]
        if isinstance(self.monitor_batch_id, Unset):
            monitor_batch_id = UNSET
        else:
            monitor_batch_id = self.monitor_batch_id

        processing_started: Union[None, Unset, str]
        if isinstance(self.processing_started, Unset):
            processing_started = UNSET
        elif isinstance(self.processing_started, datetime.datetime):
            processing_started = self.processing_started.isoformat()
        else:
            processing_started = self.processing_started

        progress_message: Union[None, Unset, str]
        if isinstance(self.progress_message, Unset):
            progress_message = UNSET
        else:
            progress_message = self.progress_message

        progress_percent = self.progress_percent

        steps_completed = self.steps_completed

        steps_total = self.steps_total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "id": id,
                "job_name": job_name,
                "project_id": project_id,
                "request_data": request_data,
                "retries": retries,
                "run_id": run_id,
                "status": status,
                "updated_at": updated_at,
            }
        )
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if failed_at is not UNSET:
            field_dict["failed_at"] = failed_at
        if migration_name is not UNSET:
            field_dict["migration_name"] = migration_name
        if monitor_batch_id is not UNSET:
            field_dict["monitor_batch_id"] = monitor_batch_id
        if processing_started is not UNSET:
            field_dict["processing_started"] = processing_started
        if progress_message is not UNSET:
            field_dict["progress_message"] = progress_message
        if progress_percent is not UNSET:
            field_dict["progress_percent"] = progress_percent
        if steps_completed is not UNSET:
            field_dict["steps_completed"] = steps_completed
        if steps_total is not UNSET:
            field_dict["steps_total"] = steps_total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.job_db_request_data import JobDBRequestData

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        job_name = d.pop("job_name")

        project_id = d.pop("project_id")

        request_data = JobDBRequestData.from_dict(d.pop("request_data"))

        retries = d.pop("retries")

        run_id = d.pop("run_id")

        status = d.pop("status")

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_completed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        def _parse_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_failed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                failed_at_type_0 = isoparse(data)

                return failed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        failed_at = _parse_failed_at(d.pop("failed_at", UNSET))

        def _parse_migration_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        migration_name = _parse_migration_name(d.pop("migration_name", UNSET))

        def _parse_monitor_batch_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        monitor_batch_id = _parse_monitor_batch_id(d.pop("monitor_batch_id", UNSET))

        def _parse_processing_started(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                processing_started_type_0 = isoparse(data)

                return processing_started_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        processing_started = _parse_processing_started(d.pop("processing_started", UNSET))

        def _parse_progress_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        progress_message = _parse_progress_message(d.pop("progress_message", UNSET))

        progress_percent = d.pop("progress_percent", UNSET)

        steps_completed = d.pop("steps_completed", UNSET)

        steps_total = d.pop("steps_total", UNSET)

        job_db = cls(
            created_at=created_at,
            id=id,
            job_name=job_name,
            project_id=project_id,
            request_data=request_data,
            retries=retries,
            run_id=run_id,
            status=status,
            updated_at=updated_at,
            completed_at=completed_at,
            error_message=error_message,
            failed_at=failed_at,
            migration_name=migration_name,
            monitor_batch_id=monitor_batch_id,
            processing_started=processing_started,
            progress_message=progress_message,
            progress_percent=progress_percent,
            steps_completed=steps_completed,
            steps_total=steps_total,
        )

        job_db.additional_properties = d
        return job_db

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
