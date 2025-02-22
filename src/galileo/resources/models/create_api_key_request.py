import datetime
from typing import Any, TypeVar, Union, cast

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
        expires_at (Union[None, Unset, datetime.datetime]): Expiry date for the API key
        project_id (Union[None, Unset, str]):
        project_role (Union[CollaboratorRole, None, Unset]):
    """

    description: str
    expires_at: Union[None, Unset, datetime.datetime] = UNSET
    project_id: Union[None, Unset, str] = UNSET
    project_role: Union[CollaboratorRole, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        project_role: Union[None, Unset, str]
        if isinstance(self.project_role, Unset):
            project_role = UNSET
        elif isinstance(self.project_role, CollaboratorRole):
            project_role = self.project_role.value
        else:
            project_role = self.project_role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"description": description})
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if project_role is not UNSET:
            field_dict["project_role"] = project_role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description")

        def _parse_expires_at(data: object) -> Union[None, Unset, datetime.datetime]:
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
            return cast(Union[None, Unset, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        def _parse_project_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_project_role(data: object) -> Union[CollaboratorRole, None, Unset]:
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
            return cast(Union[CollaboratorRole, None, Unset], data)

        project_role = _parse_project_role(d.pop("project_role", UNSET))

        create_api_key_request = cls(
            description=description, expires_at=expires_at, project_id=project_id, project_role=project_role
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
