from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_prompt import BasePrompt
    from ..models.prompt_run_settings_output import PromptRunSettingsOutput


T = TypeVar("T", bound="PlaygroundPromptResponse")


@_attrs_define
class PlaygroundPromptResponse:
    """
    Attributes:
        id (str):
        base_prompt (BasePrompt | None):
        raw (bool):
        position (int):
        template (None | str | Unset): Overrides the base prompt template if set.
        settings (PromptRunSettingsOutput | Unset): Prompt run settings.
        run_id (None | str | Unset):
    """

    id: str
    base_prompt: BasePrompt | None
    raw: bool
    position: int
    template: None | str | Unset = UNSET
    settings: PromptRunSettingsOutput | Unset = UNSET
    run_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_prompt import BasePrompt

        id = self.id

        base_prompt: dict[str, Any] | None
        if isinstance(self.base_prompt, BasePrompt):
            base_prompt = self.base_prompt.to_dict()
        else:
            base_prompt = self.base_prompt

        raw = self.raw

        position = self.position

        template: None | str | Unset
        if isinstance(self.template, Unset):
            template = UNSET
        else:
            template = self.template

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        run_id: None | str | Unset
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        else:
            run_id = self.run_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "base_prompt": base_prompt, "raw": raw, "position": position})
        if template is not UNSET:
            field_dict["template"] = template
        if settings is not UNSET:
            field_dict["settings"] = settings
        if run_id is not UNSET:
            field_dict["run_id"] = run_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_prompt import BasePrompt
        from ..models.prompt_run_settings_output import PromptRunSettingsOutput

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_base_prompt(data: object) -> BasePrompt | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                base_prompt_type_0 = BasePrompt.from_dict(data)

                return base_prompt_type_0
            except:  # noqa: E722
                pass
            return cast(BasePrompt | None, data)

        base_prompt = _parse_base_prompt(d.pop("base_prompt"))

        raw = d.pop("raw")

        position = d.pop("position")

        def _parse_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        template = _parse_template(d.pop("template", UNSET))

        _settings = d.pop("settings", UNSET)
        settings: PromptRunSettingsOutput | Unset
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = PromptRunSettingsOutput.from_dict(_settings)

        def _parse_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        playground_prompt_response = cls(
            id=id,
            base_prompt=base_prompt,
            raw=raw,
            position=position,
            template=template,
            settings=settings,
            run_id=run_id,
        )

        playground_prompt_response.additional_properties = d
        return playground_prompt_response

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
