from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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

    Attributes
    ----------
        logprobs (Union[Unset, bool]):  Default: True.
        top_logprobs (Union[Unset, int]):  Default: 5.
        echo (Union[Unset, bool]):  Default: False.
        n (Union[Unset, int]):  Default: 1.
        reasoning_effort (Union[Unset, str]):  Default: 'medium'.
        verbosity (Union[Unset, str]):  Default: 'medium'.
        deployment_name (Union[None, Unset, str]):
        model_alias (Union[Unset, str]):  Default: 'GPT-4o'.
        temperature (Union[Unset, float]):  Default: 1.0.
        max_tokens (Union[Unset, int]):  Default: 4096.
        stop_sequences (Union[None, Unset, list[str]]):
        top_p (Union[Unset, float]):  Default: 1.0.
        top_k (Union[Unset, int]):  Default: 40.
        frequency_penalty (Union[Unset, float]):  Default: 0.0.
        presence_penalty (Union[Unset, float]):  Default: 0.0.
        tools (Union[None, Unset, list['PromptRunSettingsToolsType0Item']]):
        tool_choice (Union['OpenAIToolChoice', None, Unset, str]):
        response_format (Union['PromptRunSettingsResponseFormatType0', None, Unset]):
        known_models (Union[Unset, list['Model']]):
    """

    logprobs: Union[Unset, bool] = True
    top_logprobs: Union[Unset, int] = 5
    echo: Union[Unset, bool] = False
    n: Union[Unset, int] = 1
    reasoning_effort: Union[Unset, str] = "medium"
    verbosity: Union[Unset, str] = "medium"
    deployment_name: Union[None, Unset, str] = UNSET
    model_alias: Union[Unset, str] = "GPT-4o"
    temperature: Union[Unset, float] = 1.0
    max_tokens: Union[Unset, int] = 4096
    stop_sequences: Union[None, Unset, list[str]] = UNSET
    top_p: Union[Unset, float] = 1.0
    top_k: Union[Unset, int] = 40
    frequency_penalty: Union[Unset, float] = 0.0
    presence_penalty: Union[Unset, float] = 0.0
    tools: Union[None, Unset, list["PromptRunSettingsToolsType0Item"]] = UNSET
    tool_choice: Union["OpenAIToolChoice", None, Unset, str] = UNSET
    response_format: Union["PromptRunSettingsResponseFormatType0", None, Unset] = UNSET
    known_models: Union[Unset, list["Model"]] = UNSET
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

        deployment_name: Union[None, Unset, str]
        deployment_name = UNSET if isinstance(self.deployment_name, Unset) else self.deployment_name

        model_alias = self.model_alias

        temperature = self.temperature

        max_tokens = self.max_tokens

        stop_sequences: Union[None, Unset, list[str]]
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

        tools: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)

        else:
            tools = self.tools

        tool_choice: Union[None, Unset, dict[str, Any], str]
        if isinstance(self.tool_choice, Unset):
            tool_choice = UNSET
        elif isinstance(self.tool_choice, OpenAIToolChoice):
            tool_choice = self.tool_choice.to_dict()
        else:
            tool_choice = self.tool_choice

        response_format: Union[None, Unset, dict[str, Any]]
        if isinstance(self.response_format, Unset):
            response_format = UNSET
        elif isinstance(self.response_format, PromptRunSettingsResponseFormatType0):
            response_format = self.response_format.to_dict()
        else:
            response_format = self.response_format

        known_models: Union[Unset, list[dict[str, Any]]] = UNSET
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

        def _parse_deployment_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deployment_name = _parse_deployment_name(d.pop("deployment_name", UNSET))

        model_alias = d.pop("model_alias", UNSET)

        temperature = d.pop("temperature", UNSET)

        max_tokens = d.pop("max_tokens", UNSET)

        def _parse_stop_sequences(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        stop_sequences = _parse_stop_sequences(d.pop("stop_sequences", UNSET))

        top_p = d.pop("top_p", UNSET)

        top_k = d.pop("top_k", UNSET)

        frequency_penalty = d.pop("frequency_penalty", UNSET)

        presence_penalty = d.pop("presence_penalty", UNSET)

        def _parse_tools(data: object) -> Union[None, Unset, list["PromptRunSettingsToolsType0Item"]]:
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
            return cast(Union[None, Unset, list["PromptRunSettingsToolsType0Item"]], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_tool_choice(data: object) -> Union["OpenAIToolChoice", None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return OpenAIToolChoice.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["OpenAIToolChoice", None, Unset, str], data)

        tool_choice = _parse_tool_choice(d.pop("tool_choice", UNSET))

        def _parse_response_format(data: object) -> Union["PromptRunSettingsResponseFormatType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return PromptRunSettingsResponseFormatType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["PromptRunSettingsResponseFormatType0", None, Unset], data)

        response_format = _parse_response_format(d.pop("response_format", UNSET))

        known_models = []
        _known_models = d.pop("known_models", UNSET)
        for known_models_item_data in _known_models or []:
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
