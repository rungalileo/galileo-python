from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.collaborator_role import CollaboratorRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateApiKeyRequest")


@_attrs_define
class CreateApiKeyRequest:
    """
    Attributes:
        description (str):
        expires_at (datetime.datetime | None | Unset): Expiry date for the API key
        project_id (None | str | Unset):
        project_role (CollaboratorRole | None | Unset):
        api_key (None | str | Unset): Optional pre-generated API key value. If not provided, one will be generated
            automatically. This is used for setups where the same API key needs to exist on multiple clusters.
    """

    description: str
    expires_at: datetime.datetime | None | Unset = UNSET
    project_id: None | str | Unset = UNSET
    project_role: CollaboratorRole | None | Unset = UNSET
    api_key: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

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

        api_key: None | str | Unset
        if isinstance(self.api_key, Unset):
            api_key = UNSET
        else:
            api_key = self.api_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"description": description})
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if project_role is not UNSET:
            field_dict["project_role"] = project_role
        if api_key is not UNSET:
            field_dict["api_key"] = api_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

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

        def _parse_api_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        api_key = _parse_api_key(d.pop("api_key", UNSET))

        create_api_key_request = cls(
            description=description,
            expires_at=expires_at,
            project_id=project_id,
            project_role=project_role,
            api_key=api_key,
        )

        create_api_key_request.additional_properties = d
        return create_api_key_request

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
