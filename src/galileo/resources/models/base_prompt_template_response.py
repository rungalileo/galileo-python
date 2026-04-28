from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_prompt_template_version_response import BasePromptTemplateVersionResponse
    from ..models.name import Name
    from ..models.permission import Permission
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="BasePromptTemplateResponse")


@_attrs_define
class BasePromptTemplateResponse:
    """Response from API to get a prompt template version.

    Attributes
    ----------
        id (str):
        name (Name | str):
        template (str):
        selected_version (BasePromptTemplateVersionResponse): Base response from API for a prompt template version.
        selected_version_id (str):
        all_available_versions (list[int]):
        total_versions (int):
        max_version (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        created_by_user (None | UserInfo):
        permissions (list[Permission] | Unset):
        all_versions (list[BasePromptTemplateVersionResponse] | Unset):
    """

    id: str
    name: Name | str
    template: str
    selected_version: BasePromptTemplateVersionResponse
    selected_version_id: str
    all_available_versions: list[int]
    total_versions: int
    max_version: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by_user: None | UserInfo
    permissions: list[Permission] | Unset = UNSET
    all_versions: list[BasePromptTemplateVersionResponse] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.name import Name
        from ..models.user_info import UserInfo

        id = self.id

        name: dict[str, Any] | str
        name = self.name.to_dict() if isinstance(self.name, Name) else self.name

        template = self.template

        selected_version = self.selected_version.to_dict()

        selected_version_id = self.selected_version_id

        all_available_versions = self.all_available_versions

        total_versions = self.total_versions

        max_version = self.max_version

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        created_by_user: dict[str, Any] | None
        if isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        permissions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        all_versions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.all_versions, Unset):
            all_versions = []
            for all_versions_item_data in self.all_versions:
                all_versions_item = all_versions_item_data.to_dict()
                all_versions.append(all_versions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "template": template,
                "selected_version": selected_version,
                "selected_version_id": selected_version_id,
                "all_available_versions": all_available_versions,
                "total_versions": total_versions,
                "max_version": max_version,
                "created_at": created_at,
                "updated_at": updated_at,
                "created_by_user": created_by_user,
            }
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if all_versions is not UNSET:
            field_dict["all_versions"] = all_versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_prompt_template_version_response import BasePromptTemplateVersionResponse
        from ..models.name import Name
        from ..models.permission import Permission
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_name(data: object) -> Name | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Name.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Name | str, data)

        name = _parse_name(d.pop("name"))

        template = d.pop("template")

        selected_version = BasePromptTemplateVersionResponse.from_dict(d.pop("selected_version"))

        selected_version_id = d.pop("selected_version_id")

        all_available_versions = cast(list[int], d.pop("all_available_versions"))

        total_versions = d.pop("total_versions")

        max_version = d.pop("max_version")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_created_by_user(data: object) -> None | UserInfo:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return UserInfo.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | UserInfo, data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user"))

        _permissions = d.pop("permissions", UNSET)
        permissions: list[Permission] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = Permission.from_dict(permissions_item_data)

                permissions.append(permissions_item)

        _all_versions = d.pop("all_versions", UNSET)
        all_versions: list[BasePromptTemplateVersionResponse] | Unset = UNSET
        if _all_versions is not UNSET:
            all_versions = []
            for all_versions_item_data in _all_versions:
                all_versions_item = BasePromptTemplateVersionResponse.from_dict(all_versions_item_data)

                all_versions.append(all_versions_item)

        base_prompt_template_response = cls(
            id=id,
            name=name,
            template=template,
            selected_version=selected_version,
            selected_version_id=selected_version_id,
            all_available_versions=all_available_versions,
            total_versions=total_versions,
            max_version=max_version,
            created_at=created_at,
            updated_at=updated_at,
            created_by_user=created_by_user,
            permissions=permissions,
            all_versions=all_versions,
        )

        base_prompt_template_response.additional_properties = d
        return base_prompt_template_response

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
