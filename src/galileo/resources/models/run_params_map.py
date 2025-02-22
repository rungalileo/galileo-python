from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunParamsMap")


@_attrs_define
class RunParamsMap:
    """Maps the internal settings parameters (left) to the serialized parameters (right) we want to send in the API
    requests.

        Attributes:
            api_version (Union[None, Unset, str]):
            deployment_name (Union[None, Unset, str]):
            echo (Union[None, Unset, str]):
            frequency_penalty (Union[None, Unset, str]):
            logprobs (Union[None, Unset, str]):
            max_tokens (Union[None, Unset, str]):
            model (Union[None, Unset, str]):
            n (Union[None, Unset, str]):
            presence_penalty (Union[None, Unset, str]):
            response_format (Union[None, Unset, str]):
            stop_sequences (Union[None, Unset, str]):
            temperature (Union[None, Unset, str]):
            tool_choice (Union[None, Unset, str]):
            tools (Union[None, Unset, str]):
            top_k (Union[None, Unset, str]):
            top_logprobs (Union[None, Unset, str]):
            top_p (Union[None, Unset, str]):
    """

    api_version: Union[None, Unset, str] = UNSET
    deployment_name: Union[None, Unset, str] = UNSET
    echo: Union[None, Unset, str] = UNSET
    frequency_penalty: Union[None, Unset, str] = UNSET
    logprobs: Union[None, Unset, str] = UNSET
    max_tokens: Union[None, Unset, str] = UNSET
    model: Union[None, Unset, str] = UNSET
    n: Union[None, Unset, str] = UNSET
    presence_penalty: Union[None, Unset, str] = UNSET
    response_format: Union[None, Unset, str] = UNSET
    stop_sequences: Union[None, Unset, str] = UNSET
    temperature: Union[None, Unset, str] = UNSET
    tool_choice: Union[None, Unset, str] = UNSET
    tools: Union[None, Unset, str] = UNSET
    top_k: Union[None, Unset, str] = UNSET
    top_logprobs: Union[None, Unset, str] = UNSET
    top_p: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_version: Union[None, Unset, str]
        if isinstance(self.api_version, Unset):
            api_version = UNSET
        else:
            api_version = self.api_version

        deployment_name: Union[None, Unset, str]
        if isinstance(self.deployment_name, Unset):
            deployment_name = UNSET
        else:
            deployment_name = self.deployment_name

        echo: Union[None, Unset, str]
        if isinstance(self.echo, Unset):
            echo = UNSET
        else:
            echo = self.echo

        frequency_penalty: Union[None, Unset, str]
        if isinstance(self.frequency_penalty, Unset):
            frequency_penalty = UNSET
        else:
            frequency_penalty = self.frequency_penalty

        logprobs: Union[None, Unset, str]
        if isinstance(self.logprobs, Unset):
            logprobs = UNSET
        else:
            logprobs = self.logprobs

        max_tokens: Union[None, Unset, str]
        if isinstance(self.max_tokens, Unset):
            max_tokens = UNSET
        else:
            max_tokens = self.max_tokens

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        n: Union[None, Unset, str]
        if isinstance(self.n, Unset):
            n = UNSET
        else:
            n = self.n

        presence_penalty: Union[None, Unset, str]
        if isinstance(self.presence_penalty, Unset):
            presence_penalty = UNSET
        else:
            presence_penalty = self.presence_penalty

        response_format: Union[None, Unset, str]
        if isinstance(self.response_format, Unset):
            response_format = UNSET
        else:
            response_format = self.response_format

        stop_sequences: Union[None, Unset, str]
        if isinstance(self.stop_sequences, Unset):
            stop_sequences = UNSET
        else:
            stop_sequences = self.stop_sequences

        temperature: Union[None, Unset, str]
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        tool_choice: Union[None, Unset, str]
        if isinstance(self.tool_choice, Unset):
            tool_choice = UNSET
        else:
            tool_choice = self.tool_choice

        tools: Union[None, Unset, str]
        if isinstance(self.tools, Unset):
            tools = UNSET
        else:
            tools = self.tools

        top_k: Union[None, Unset, str]
        if isinstance(self.top_k, Unset):
            top_k = UNSET
        else:
            top_k = self.top_k

        top_logprobs: Union[None, Unset, str]
        if isinstance(self.top_logprobs, Unset):
            top_logprobs = UNSET
        else:
            top_logprobs = self.top_logprobs

        top_p: Union[None, Unset, str]
        if isinstance(self.top_p, Unset):
            top_p = UNSET
        else:
            top_p = self.top_p

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if deployment_name is not UNSET:
            field_dict["deployment_name"] = deployment_name
        if echo is not UNSET:
            field_dict["echo"] = echo
        if frequency_penalty is not UNSET:
            field_dict["frequency_penalty"] = frequency_penalty
        if logprobs is not UNSET:
            field_dict["logprobs"] = logprobs
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if model is not UNSET:
            field_dict["model"] = model
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
        d = src_dict.copy()

        def _parse_api_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_version = _parse_api_version(d.pop("api_version", UNSET))

        def _parse_deployment_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deployment_name = _parse_deployment_name(d.pop("deployment_name", UNSET))

        def _parse_echo(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        echo = _parse_echo(d.pop("echo", UNSET))

        def _parse_frequency_penalty(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        frequency_penalty = _parse_frequency_penalty(d.pop("frequency_penalty", UNSET))

        def _parse_logprobs(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        logprobs = _parse_logprobs(d.pop("logprobs", UNSET))

        def _parse_max_tokens(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        max_tokens = _parse_max_tokens(d.pop("max_tokens", UNSET))

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_n(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        n = _parse_n(d.pop("n", UNSET))

        def _parse_presence_penalty(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        presence_penalty = _parse_presence_penalty(d.pop("presence_penalty", UNSET))

        def _parse_response_format(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        response_format = _parse_response_format(d.pop("response_format", UNSET))

        def _parse_stop_sequences(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        stop_sequences = _parse_stop_sequences(d.pop("stop_sequences", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_tool_choice(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tool_choice = _parse_tool_choice(d.pop("tool_choice", UNSET))

        def _parse_tools(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_top_k(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        top_k = _parse_top_k(d.pop("top_k", UNSET))

        def _parse_top_logprobs(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        top_logprobs = _parse_top_logprobs(d.pop("top_logprobs", UNSET))

        def _parse_top_p(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        top_p = _parse_top_p(d.pop("top_p", UNSET))

        run_params_map = cls(
            api_version=api_version,
            deployment_name=deployment_name,
            echo=echo,
            frequency_penalty=frequency_penalty,
            logprobs=logprobs,
            max_tokens=max_tokens,
            model=model,
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

        run_params_map.additional_properties = d
        return run_params_map

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
