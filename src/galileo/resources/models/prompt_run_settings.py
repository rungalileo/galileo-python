from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model import Model
    from ..models.open_ai_tool_choice import OpenAIToolChoice
    from ..models.prompt_run_settings_response_format_type_0 import PromptRunSettingsResponseFormatType0
    from ..models.prompt_run_settings_tools_type_0_item import PromptRunSettingsToolsType0Item


T = TypeVar("T", bound="PromptRunSettings")


@_attrs_define
class PromptRunSettings:
    """Prompt run settings.

    Attributes:
        logprobs (bool | Unset):  Default: True.
        top_logprobs (int | Unset):  Default: 5.
        echo (bool | Unset):  Default: False.
        n (int | Unset):  Default: 1.
        reasoning_effort (str | Unset):  Default: 'medium'.
        verbosity (str | Unset):  Default: 'medium'.
        deployment_name (None | str | Unset):
        model_alias (str | Unset):  Default: 'gpt-5.1'.
        temperature (float | None | Unset):
        max_tokens (int | Unset):  Default: 4096.
        stop_sequences (list[str] | None | Unset):
        top_p (float | Unset):  Default: 1.0.
        top_k (int | Unset):  Default: 40.
        frequency_penalty (float | Unset):  Default: 0.0.
        presence_penalty (float | Unset):  Default: 0.0.
        tools (list[PromptRunSettingsToolsType0Item] | None | Unset):
        tool_choice (None | OpenAIToolChoice | str | Unset):
        response_format (None | PromptRunSettingsResponseFormatType0 | Unset):
        known_models (list[Model] | Unset):
    """

    logprobs: bool | Unset = True
    top_logprobs: int | Unset = 5
    echo: bool | Unset = False
    n: int | Unset = 1
    reasoning_effort: str | Unset = "medium"
    verbosity: str | Unset = "medium"
    deployment_name: None | str | Unset = UNSET
    model_alias: str | Unset = "gpt-5.1"
    temperature: float | None | Unset = UNSET
    max_tokens: int | Unset = 4096
    stop_sequences: list[str] | None | Unset = UNSET
    top_p: float | Unset = 1.0
    top_k: int | Unset = 40
    frequency_penalty: float | Unset = 0.0
    presence_penalty: float | Unset = 0.0
    tools: list[PromptRunSettingsToolsType0Item] | None | Unset = UNSET
    tool_choice: None | OpenAIToolChoice | str | Unset = UNSET
    response_format: None | PromptRunSettingsResponseFormatType0 | Unset = UNSET
    known_models: list[Model] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.open_ai_tool_choice import OpenAIToolChoice
        from ..models.prompt_run_settings_response_format_type_0 import PromptRunSettingsResponseFormatType0

        logprobs = self.logprobs

        top_logprobs = self.top_logprobs

        echo = self.echo

        n = self.n

        reasoning_effort = self.reasoning_effort

        verbosity = self.verbosity

        deployment_name: None | str | Unset
        if isinstance(self.deployment_name, Unset):
            deployment_name = UNSET
        else:
            deployment_name = self.deployment_name

        model_alias = self.model_alias

        temperature: float | None | Unset
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        max_tokens = self.max_tokens

        stop_sequences: list[str] | None | Unset
        if isinstance(self.stop_sequences, Unset):
            stop_sequences = UNSET
        elif isinstance(self.stop_sequences, list):
            stop_sequences = self.stop_sequences

        else:
            stop_sequences = self.stop_sequences

        top_p = self.top_p

        top_k = self.top_k

        frequency_penalty = self.frequency_penalty

        presence_penalty = self.presence_penalty

        tools: list[dict[str, Any]] | None | Unset
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)

        else:
            tools = self.tools

        tool_choice: dict[str, Any] | None | str | Unset
        if isinstance(self.tool_choice, Unset):
            tool_choice = UNSET
        elif isinstance(self.tool_choice, OpenAIToolChoice):
            tool_choice = self.tool_choice.to_dict()
        else:
            tool_choice = self.tool_choice

        response_format: dict[str, Any] | None | Unset
        if isinstance(self.response_format, Unset):
            response_format = UNSET
        elif isinstance(self.response_format, PromptRunSettingsResponseFormatType0):
            response_format = self.response_format.to_dict()
        else:
            response_format = self.response_format

        known_models: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.known_models, Unset):
            known_models = []
            for known_models_item_data in self.known_models:
                known_models_item = known_models_item_data.to_dict()
                known_models.append(known_models_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if logprobs is not UNSET:
            field_dict["logprobs"] = logprobs
        if top_logprobs is not UNSET:
            field_dict["top_logprobs"] = top_logprobs
        if echo is not UNSET:
            field_dict["echo"] = echo
        if n is not UNSET:
            field_dict["n"] = n
        if reasoning_effort is not UNSET:
            field_dict["reasoning_effort"] = reasoning_effort
        if verbosity is not UNSET:
            field_dict["verbosity"] = verbosity
        if deployment_name is not UNSET:
            field_dict["deployment_name"] = deployment_name
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if stop_sequences is not UNSET:
            field_dict["stop_sequences"] = stop_sequences
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if top_k is not UNSET:
            field_dict["top_k"] = top_k
        if frequency_penalty is not UNSET:
            field_dict["frequency_penalty"] = frequency_penalty
        if presence_penalty is not UNSET:
            field_dict["presence_penalty"] = presence_penalty
        if tools is not UNSET:
            field_dict["tools"] = tools
        if tool_choice is not UNSET:
            field_dict["tool_choice"] = tool_choice
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if known_models is not UNSET:
            field_dict["known_models"] = known_models

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model import Model
        from ..models.open_ai_tool_choice import OpenAIToolChoice
        from ..models.prompt_run_settings_response_format_type_0 import PromptRunSettingsResponseFormatType0
        from ..models.prompt_run_settings_tools_type_0_item import PromptRunSettingsToolsType0Item

        d = dict(src_dict)
        logprobs = d.pop("logprobs", UNSET)

        top_logprobs = d.pop("top_logprobs", UNSET)

        echo = d.pop("echo", UNSET)

        n = d.pop("n", UNSET)

        reasoning_effort = d.pop("reasoning_effort", UNSET)

        verbosity = d.pop("verbosity", UNSET)

        def _parse_deployment_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        deployment_name = _parse_deployment_name(d.pop("deployment_name", UNSET))

        model_alias = d.pop("model_alias", UNSET)

        def _parse_temperature(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        max_tokens = d.pop("max_tokens", UNSET)

        def _parse_stop_sequences(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                stop_sequences_type_0 = cast(list[str], data)

                return stop_sequences_type_0
            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        stop_sequences = _parse_stop_sequences(d.pop("stop_sequences", UNSET))

        top_p = d.pop("top_p", UNSET)

        top_k = d.pop("top_k", UNSET)

        frequency_penalty = d.pop("frequency_penalty", UNSET)

        presence_penalty = d.pop("presence_penalty", UNSET)

        def _parse_tools(data: object) -> list[PromptRunSettingsToolsType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0 = []
                _tools_type_0 = data
                for tools_type_0_item_data in _tools_type_0:
                    tools_type_0_item = PromptRunSettingsToolsType0Item.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except:  # noqa: E722
                pass
            return cast(list[PromptRunSettingsToolsType0Item] | None | Unset, data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_tool_choice(data: object) -> None | OpenAIToolChoice | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tool_choice_type_1 = OpenAIToolChoice.from_dict(data)

                return tool_choice_type_1
            except:  # noqa: E722
                pass
            return cast(None | OpenAIToolChoice | str | Unset, data)

        tool_choice = _parse_tool_choice(d.pop("tool_choice", UNSET))

        def _parse_response_format(data: object) -> None | PromptRunSettingsResponseFormatType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_format_type_0 = PromptRunSettingsResponseFormatType0.from_dict(data)

                return response_format_type_0
            except:  # noqa: E722
                pass
            return cast(None | PromptRunSettingsResponseFormatType0 | Unset, data)

        response_format = _parse_response_format(d.pop("response_format", UNSET))

        _known_models = d.pop("known_models", UNSET)
        known_models: list[Model] | Unset = UNSET
        if _known_models is not UNSET:
            known_models = []
            for known_models_item_data in _known_models:
                known_models_item = Model.from_dict(known_models_item_data)

                known_models.append(known_models_item)

        prompt_run_settings = cls(
            logprobs=logprobs,
            top_logprobs=top_logprobs,
            echo=echo,
            n=n,
            reasoning_effort=reasoning_effort,
            verbosity=verbosity,
            deployment_name=deployment_name,
            model_alias=model_alias,
            temperature=temperature,
            max_tokens=max_tokens,
            stop_sequences=stop_sequences,
            top_p=top_p,
            top_k=top_k,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            tools=tools,
            tool_choice=tool_choice,
            response_format=response_format,
            known_models=known_models,
        )

        prompt_run_settings.additional_properties = d
        return prompt_run_settings

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
