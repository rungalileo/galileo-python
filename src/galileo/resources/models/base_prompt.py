from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission
    from ..models.prompt_run_settings_output import PromptRunSettingsOutput


T = TypeVar("T", bound="BasePrompt")


@_attrs_define
class BasePrompt:
    """
    Attributes:
        id (str):
        version (int):
        version_id (str):
        name (str):
        template (str):
        permissions (list[Permission] | Unset):
        settings (PromptRunSettingsOutput | Unset): Prompt run settings.
        raw (bool | Unset):  Default: False.
    """

    id: str
    version: int
    version_id: str
    name: str
    template: str
    permissions: list[Permission] | Unset = UNSET
    settings: PromptRunSettingsOutput | Unset = UNSET
    raw: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        version = self.version

        version_id = self.version_id

        name = self.name

        template = self.template

        permissions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        raw = self.raw

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "version": version, "version_id": version_id, "name": name, "template": template})
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if settings is not UNSET:
            field_dict["settings"] = settings
        if raw is not UNSET:
            field_dict["raw"] = raw

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission import Permission
        from ..models.prompt_run_settings_output import PromptRunSettingsOutput

        d = dict(src_dict)
        id = d.pop("id")

        version = d.pop("version")

        version_id = d.pop("version_id")

        name = d.pop("name")

        template = d.pop("template")

        _permissions = d.pop("permissions", UNSET)
        permissions: list[Permission] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = Permission.from_dict(permissions_item_data)

                permissions.append(permissions_item)

        _settings = d.pop("settings", UNSET)
        settings: PromptRunSettingsOutput | Unset
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = PromptRunSettingsOutput.from_dict(_settings)

        raw = d.pop("raw", UNSET)

        base_prompt = cls(
            id=id,
            version=version,
            version_id=version_id,
            name=name,
            template=template,
            permissions=permissions,
            settings=settings,
            raw=raw,
        )

        base_prompt.additional_properties = d
        return base_prompt

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
