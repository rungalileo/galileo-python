from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.org_job_db_request_data import OrgJobDBRequestData


T = TypeVar("T", bound="OrgJobDB")


@_attrs_define
class OrgJobDB:
    """Response schema for org jobs.

    Attributes:
        id (str):
        organization_id (str):
        job_name (str):
        status (str):
        request_data (OrgJobDBRequestData):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        error_message (None | str | Unset):
        created_by (None | str | Unset):
    """

    id: str
    organization_id: str
    job_name: str
    status: str
    request_data: OrgJobDBRequestData
    created_at: datetime.datetime
    updated_at: datetime.datetime
    error_message: None | str | Unset = UNSET
    created_by: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        organization_id = self.organization_id

        job_name = self.job_name

        status = self.status

        request_data = self.request_data.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        created_by: None | str | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organization_id": organization_id,
                "job_name": job_name,
                "status": status,
                "request_data": request_data,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if created_by is not UNSET:
            field_dict["created_by"] = created_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.org_job_db_request_data import OrgJobDBRequestData

        d = dict(src_dict)
        id = d.pop("id")

        organization_id = d.pop("organization_id")

        job_name = d.pop("job_name")

        status = d.pop("status")

        request_data = OrgJobDBRequestData.from_dict(d.pop("request_data"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_created_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        org_job_db = cls(
            id=id,
            organization_id=organization_id,
            job_name=job_name,
            status=status,
            request_data=request_data,
            created_at=created_at,
            updated_at=updated_at,
            error_message=error_message,
            created_by=created_by,
        )

        org_job_db.additional_properties = d
        return org_job_db

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
