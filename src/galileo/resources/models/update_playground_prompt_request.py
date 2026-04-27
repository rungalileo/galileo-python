from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.prompt_run_settings import PromptRunSettings


T = TypeVar("T", bound="UpdatePlaygroundPromptRequest")


@_attrs_define
class UpdatePlaygroundPromptRequest:
    """
    Attributes:
        base_prompt_template_version_id (None | str | Unset):
        template (None | str | Unset):
        settings (None | PromptRunSettings | Unset):
        raw (bool | None | Unset):
    """

    base_prompt_template_version_id: None | str | Unset = UNSET
    template: None | str | Unset = UNSET
    settings: None | PromptRunSettings | Unset = UNSET
    raw: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.prompt_run_settings import PromptRunSettings

        base_prompt_template_version_id: None | str | Unset
        if isinstance(self.base_prompt_template_version_id, Unset):
            base_prompt_template_version_id = UNSET
        else:
            base_prompt_template_version_id = self.base_prompt_template_version_id

        template: None | str | Unset
        if isinstance(self.template, Unset):
            template = UNSET
        else:
            template = self.template

        settings: dict[str, Any] | None | Unset
        if isinstance(self.settings, Unset):
            settings = UNSET
        elif isinstance(self.settings, PromptRunSettings):
            settings = self.settings.to_dict()
        else:
            settings = self.settings

        raw: bool | None | Unset
        if isinstance(self.raw, Unset):
            raw = UNSET
        else:
            raw = self.raw

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base_prompt_template_version_id is not UNSET:
            field_dict["base_prompt_template_version_id"] = base_prompt_template_version_id
        if template is not UNSET:
            field_dict["template"] = template
        if settings is not UNSET:
            field_dict["settings"] = settings
        if raw is not UNSET:
            field_dict["raw"] = raw

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.prompt_run_settings import PromptRunSettings

        d = dict(src_dict)

        def _parse_base_prompt_template_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        base_prompt_template_version_id = _parse_base_prompt_template_version_id(
            d.pop("base_prompt_template_version_id", UNSET)
        )

        def _parse_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        template = _parse_template(d.pop("template", UNSET))

        def _parse_settings(data: object) -> None | PromptRunSettings | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                settings_type_0 = PromptRunSettings.from_dict(data)

                return settings_type_0
            except:  # noqa: E722
                pass
            return cast(None | PromptRunSettings | Unset, data)

        settings = _parse_settings(d.pop("settings", UNSET))

        def _parse_raw(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        raw = _parse_raw(d.pop("raw", UNSET))

        update_playground_prompt_request = cls(
            base_prompt_template_version_id=base_prompt_template_version_id,
            template=template,
            settings=settings,
            raw=raw,
        )

        update_playground_prompt_request.additional_properties = d
        return update_playground_prompt_request

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
