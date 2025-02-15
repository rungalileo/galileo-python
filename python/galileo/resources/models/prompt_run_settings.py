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

    Attributes:
        deployment_name (Union[None, Unset, str]):
        echo (Union[Unset, bool]):  Default: False.
        frequency_penalty (Union[Unset, float]):  Default: 0.0.
        known_models (Union[Unset, list['Model']]):
        logprobs (Union[Unset, bool]):  Default: True.
        max_tokens (Union[Unset, int]):  Default: 256.
        model_alias (Union[Unset, str]):  Default: 'ChatGPT (4K context)'.
        n (Union[Unset, int]):  Default: 1.
        presence_penalty (Union[Unset, float]):  Default: 0.0.
        response_format (Union['PromptRunSettingsResponseFormatType0', None, Unset]):
        stop_sequences (Union[None, Unset, list[str]]):
        temperature (Union[Unset, float]):  Default: 1.0.
        tool_choice (Union['OpenAIToolChoice', None, Unset, str]):
        tools (Union[None, Unset, list['PromptRunSettingsToolsType0Item']]):
        top_k (Union[Unset, int]):  Default: 40.
        top_logprobs (Union[Unset, int]):  Default: 5.
        top_p (Union[Unset, float]):  Default: 1.0.
    """

    deployment_name: Union[None, Unset, str] = UNSET
    echo: Union[Unset, bool] = False
    frequency_penalty: Union[Unset, float] = 0.0
    known_models: Union[Unset, list["Model"]] = UNSET
    logprobs: Union[Unset, bool] = True
    max_tokens: Union[Unset, int] = 256
    model_alias: Union[Unset, str] = "ChatGPT (4K context)"
    n: Union[Unset, int] = 1
    presence_penalty: Union[Unset, float] = 0.0
    response_format: Union["PromptRunSettingsResponseFormatType0", None, Unset] = UNSET
    stop_sequences: Union[None, Unset, list[str]] = UNSET
    temperature: Union[Unset, float] = 1.0
    tool_choice: Union["OpenAIToolChoice", None, Unset, str] = UNSET
    tools: Union[None, Unset, list["PromptRunSettingsToolsType0Item"]] = UNSET
    top_k: Union[Unset, int] = 40
    top_logprobs: Union[Unset, int] = 5
    top_p: Union[Unset, float] = 1.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.open_ai_tool_choice import OpenAIToolChoice
        from ..models.prompt_run_settings_response_format_type_0 import PromptRunSettingsResponseFormatType0

        deployment_name: Union[None, Unset, str]
        if isinstance(self.deployment_name, Unset):
            deployment_name = UNSET
        else:
            deployment_name = self.deployment_name

        echo = self.echo

        frequency_penalty = self.frequency_penalty

        known_models: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.known_models, Unset):
            known_models = []
            for known_models_item_data in self.known_models:
                known_models_item = known_models_item_data.to_dict()
                known_models.append(known_models_item)

        logprobs = self.logprobs

        max_tokens = self.max_tokens

        model_alias = self.model_alias

        n = self.n

        presence_penalty = self.presence_penalty

        response_format: Union[None, Unset, dict[str, Any]]
        if isinstance(self.response_format, Unset):
            response_format = UNSET
        elif isinstance(self.response_format, PromptRunSettingsResponseFormatType0):
            response_format = self.response_format.to_dict()
        else:
            response_format = self.response_format

        stop_sequences: Union[None, Unset, list[str]]
        if isinstance(self.stop_sequences, Unset):
            stop_sequences = UNSET
        elif isinstance(self.stop_sequences, list):
            stop_sequences = self.stop_sequences

        else:
            stop_sequences = self.stop_sequences

        temperature = self.temperature

        tool_choice: Union[None, Unset, dict[str, Any], str]
        if isinstance(self.tool_choice, Unset):
            tool_choice = UNSET
        elif isinstance(self.tool_choice, OpenAIToolChoice):
            tool_choice = self.tool_choice.to_dict()
        else:
            tool_choice = self.tool_choice

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

        top_k = self.top_k

        top_logprobs = self.top_logprobs

        top_p = self.top_p

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deployment_name is not UNSET:
            field_dict["deployment_name"] = deployment_name
        if echo is not UNSET:
            field_dict["echo"] = echo
        if frequency_penalty is not UNSET:
            field_dict["frequency_penalty"] = frequency_penalty
        if known_models is not UNSET:
            field_dict["known_models"] = known_models
        if logprobs is not UNSET:
            field_dict["logprobs"] = logprobs
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if n is not UNSET:
            field_dict["n"] = n
        if presence_penalty is not UNSET:
            field_dict["presence_penalty"] = presence_penalty
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if stop_sequences is not UNSET:
            field_dict["stop_sequences"] = stop_sequences
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if tool_choice is not UNSET:
            field_dict["tool_choice"] = tool_choice
        if tools is not UNSET:
            field_dict["tools"] = tools
        if top_k is not UNSET:
            field_dict["top_k"] = top_k
        if top_logprobs is not UNSET:
            field_dict["top_logprobs"] = top_logprobs
        if top_p is not UNSET:
            field_dict["top_p"] = top_p

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.model import Model
        from ..models.open_ai_tool_choice import OpenAIToolChoice
        from ..models.prompt_run_settings_response_format_type_0 import PromptRunSettingsResponseFormatType0
        from ..models.prompt_run_settings_tools_type_0_item import PromptRunSettingsToolsType0Item

        d = src_dict.copy()

        def _parse_deployment_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deployment_name = _parse_deployment_name(d.pop("deployment_name", UNSET))

        echo = d.pop("echo", UNSET)

        frequency_penalty = d.pop("frequency_penalty", UNSET)

        known_models = []
        _known_models = d.pop("known_models", UNSET)
        for known_models_item_data in _known_models or []:
            known_models_item = Model.from_dict(known_models_item_data)

            known_models.append(known_models_item)

        logprobs = d.pop("logprobs", UNSET)

        max_tokens = d.pop("max_tokens", UNSET)

        model_alias = d.pop("model_alias", UNSET)

        n = d.pop("n", UNSET)

        presence_penalty = d.pop("presence_penalty", UNSET)

        def _parse_response_format(data: object) -> Union["PromptRunSettingsResponseFormatType0", None, Unset]:
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
            return cast(Union["PromptRunSettingsResponseFormatType0", None, Unset], data)

        response_format = _parse_response_format(d.pop("response_format", UNSET))

        def _parse_stop_sequences(data: object) -> Union[None, Unset, list[str]]:
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
            return cast(Union[None, Unset, list[str]], data)

        stop_sequences = _parse_stop_sequences(d.pop("stop_sequences", UNSET))

        temperature = d.pop("temperature", UNSET)

        def _parse_tool_choice(data: object) -> Union["OpenAIToolChoice", None, Unset, str]:
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
            return cast(Union["OpenAIToolChoice", None, Unset, str], data)

        tool_choice = _parse_tool_choice(d.pop("tool_choice", UNSET))

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

        top_k = d.pop("top_k", UNSET)

        top_logprobs = d.pop("top_logprobs", UNSET)

        top_p = d.pop("top_p", UNSET)

        prompt_run_settings = cls(
            deployment_name=deployment_name,
            echo=echo,
            frequency_penalty=frequency_penalty,
            known_models=known_models,
            logprobs=logprobs,
            max_tokens=max_tokens,
            model_alias=model_alias,
            n=n,
            presence_penalty=presence_penalty,
            response_format=response_format,
            stop_sequences=stop_sequences,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_k=top_k,
            top_logprobs=top_logprobs,
            top_p=top_p,
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
