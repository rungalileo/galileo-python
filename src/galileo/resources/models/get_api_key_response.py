from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.collaborator_role import CollaboratorRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetApiKeyResponse")


@_attrs_define
class GetApiKeyResponse:
    """
    Attributes:
        id (str):
        description (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        created_by (str):
        truncated (str):
        expires_at (datetime.datetime | None | Unset):
        last_used (datetime.datetime | None | Unset):
        project_id (None | str | Unset):
        project_role (CollaboratorRole | None | Unset):
    """

    id: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: str
    truncated: str
    expires_at: datetime.datetime | None | Unset = UNSET
    last_used: datetime.datetime | None | Unset = UNSET
    project_id: None | str | Unset = UNSET
    project_role: CollaboratorRole | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        description = self.description

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        created_by = self.created_by

        truncated = self.truncated

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        last_used: None | str | Unset
        if isinstance(self.last_used, Unset):
            last_used = UNSET
        elif isinstance(self.last_used, datetime.datetime):
            last_used = self.last_used.isoformat()
        else:
            last_used = self.last_used

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        project_role: None | str | Unset
        if isinstance(self.project_role, Unset):
            project_role = UNSET
        elif isinstance(self.project_role, CollaboratorRole):
            project_role = self.project_role.value
        else:
            project_role = self.project_role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "description": description,
                "created_at": created_at,
                "updated_at": updated_at,
                "created_by": created_by,
                "truncated": truncated,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if last_used is not UNSET:
            field_dict["last_used"] = last_used
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if project_role is not UNSET:
            field_dict["project_role"] = project_role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        description = d.pop("description")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        created_by = d.pop("created_by")

        truncated = d.pop("truncated")

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        def _parse_last_used(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_type_0 = isoparse(data)

                return last_used_type_0
            except:  # noqa: E722
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_used = _parse_last_used(d.pop("last_used", UNSET))

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_project_role(data: object) -> CollaboratorRole | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_role_type_0 = CollaboratorRole(data)

                return project_role_type_0
            except:  # noqa: E722
                pass
            return cast(CollaboratorRole | None | Unset, data)

        project_role = _parse_project_role(d.pop("project_role", UNSET))

        get_api_key_response = cls(
            id=id,
            description=description,
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            truncated=truncated,
            expires_at=expires_at,
            last_used=last_used,
            project_id=project_id,
            project_role=project_role,
        )

        get_api_key_response.additional_properties = d
        return get_api_key_response

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
