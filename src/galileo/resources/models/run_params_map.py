from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunParamsMap")


@_attrs_define
class RunParamsMap:
    """Maps the internal settings parameters (left) to the serialized parameters (right) we want to send in the API
    requests.

    Attributes
    ----------
            model (Union[None, Unset, str]):
            temperature (Union[None, Unset, str]):
            max_tokens (Union[None, Unset, str]):
            stop_sequences (Union[None, Unset, str]):
            top_p (Union[None, Unset, str]):
            top_k (Union[None, Unset, str]):
            frequency_penalty (Union[None, Unset, str]):
            presence_penalty (Union[None, Unset, str]):
            echo (Union[None, Unset, str]):
            logprobs (Union[None, Unset, str]):
            top_logprobs (Union[None, Unset, str]):
            n (Union[None, Unset, str]):
            api_version (Union[None, Unset, str]):
            tools (Union[None, Unset, str]):
            tool_choice (Union[None, Unset, str]):
            response_format (Union[None, Unset, str]):
            reasoning_effort (Union[None, Unset, str]):
            verbosity (Union[None, Unset, str]):
            deployment_name (Union[None, Unset, str]):
    """

    model: Union[None, Unset, str] = UNSET
    temperature: Union[None, Unset, str] = UNSET
    max_tokens: Union[None, Unset, str] = UNSET
    stop_sequences: Union[None, Unset, str] = UNSET
    top_p: Union[None, Unset, str] = UNSET
    top_k: Union[None, Unset, str] = UNSET
    frequency_penalty: Union[None, Unset, str] = UNSET
    presence_penalty: Union[None, Unset, str] = UNSET
    echo: Union[None, Unset, str] = UNSET
    logprobs: Union[None, Unset, str] = UNSET
    top_logprobs: Union[None, Unset, str] = UNSET
    n: Union[None, Unset, str] = UNSET
    api_version: Union[None, Unset, str] = UNSET
    tools: Union[None, Unset, str] = UNSET
    tool_choice: Union[None, Unset, str] = UNSET
    response_format: Union[None, Unset, str] = UNSET
    reasoning_effort: Union[None, Unset, str] = UNSET
    verbosity: Union[None, Unset, str] = UNSET
    deployment_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model: Union[None, Unset, str]
        model = UNSET if isinstance(self.model, Unset) else self.model

        temperature: Union[None, Unset, str]
        temperature = UNSET if isinstance(self.temperature, Unset) else self.temperature

        max_tokens: Union[None, Unset, str]
        max_tokens = UNSET if isinstance(self.max_tokens, Unset) else self.max_tokens

        stop_sequences: Union[None, Unset, str]
        stop_sequences = UNSET if isinstance(self.stop_sequences, Unset) else self.stop_sequences

        top_p: Union[None, Unset, str]
        top_p = UNSET if isinstance(self.top_p, Unset) else self.top_p

        top_k: Union[None, Unset, str]
        top_k = UNSET if isinstance(self.top_k, Unset) else self.top_k

        frequency_penalty: Union[None, Unset, str]
        frequency_penalty = UNSET if isinstance(self.frequency_penalty, Unset) else self.frequency_penalty

        presence_penalty: Union[None, Unset, str]
        presence_penalty = UNSET if isinstance(self.presence_penalty, Unset) else self.presence_penalty

        echo: Union[None, Unset, str]
        echo = UNSET if isinstance(self.echo, Unset) else self.echo

        logprobs: Union[None, Unset, str]
        logprobs = UNSET if isinstance(self.logprobs, Unset) else self.logprobs

        top_logprobs: Union[None, Unset, str]
        top_logprobs = UNSET if isinstance(self.top_logprobs, Unset) else self.top_logprobs

        n: Union[None, Unset, str]
        n = UNSET if isinstance(self.n, Unset) else self.n

        api_version: Union[None, Unset, str]
        api_version = UNSET if isinstance(self.api_version, Unset) else self.api_version

        tools: Union[None, Unset, str]
        tools = UNSET if isinstance(self.tools, Unset) else self.tools

        tool_choice: Union[None, Unset, str]
        tool_choice = UNSET if isinstance(self.tool_choice, Unset) else self.tool_choice

        response_format: Union[None, Unset, str]
        response_format = UNSET if isinstance(self.response_format, Unset) else self.response_format

        reasoning_effort: Union[None, Unset, str]
        reasoning_effort = UNSET if isinstance(self.reasoning_effort, Unset) else self.reasoning_effort

        verbosity: Union[None, Unset, str]
        verbosity = UNSET if isinstance(self.verbosity, Unset) else self.verbosity

        deployment_name: Union[None, Unset, str]
        deployment_name = UNSET if isinstance(self.deployment_name, Unset) else self.deployment_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if model is not UNSET:
            field_dict["model"] = model
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
        if echo is not UNSET:
            field_dict["echo"] = echo
        if logprobs is not UNSET:
            field_dict["logprobs"] = logprobs
        if top_logprobs is not UNSET:
            field_dict["top_logprobs"] = top_logprobs
        if n is not UNSET:
            field_dict["n"] = n
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if tools is not UNSET:
            field_dict["tools"] = tools
        if tool_choice is not UNSET:
            field_dict["tool_choice"] = tool_choice
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if reasoning_effort is not UNSET:
            field_dict["reasoning_effort"] = reasoning_effort
        if verbosity is not UNSET:
            field_dict["verbosity"] = verbosity
        if deployment_name is not UNSET:
            field_dict["deployment_name"] = deployment_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_max_tokens(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        max_tokens = _parse_max_tokens(d.pop("max_tokens", UNSET))

        def _parse_stop_sequences(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        stop_sequences = _parse_stop_sequences(d.pop("stop_sequences", UNSET))

        def _parse_top_p(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        top_p = _parse_top_p(d.pop("top_p", UNSET))

        def _parse_top_k(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        top_k = _parse_top_k(d.pop("top_k", UNSET))

        def _parse_frequency_penalty(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        frequency_penalty = _parse_frequency_penalty(d.pop("frequency_penalty", UNSET))

        def _parse_presence_penalty(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        presence_penalty = _parse_presence_penalty(d.pop("presence_penalty", UNSET))

        def _parse_echo(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        echo = _parse_echo(d.pop("echo", UNSET))

        def _parse_logprobs(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        logprobs = _parse_logprobs(d.pop("logprobs", UNSET))

        def _parse_top_logprobs(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        top_logprobs = _parse_top_logprobs(d.pop("top_logprobs", UNSET))

        def _parse_n(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        n = _parse_n(d.pop("n", UNSET))

        def _parse_api_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_version = _parse_api_version(d.pop("api_version", UNSET))

        def _parse_tools(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_tool_choice(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tool_choice = _parse_tool_choice(d.pop("tool_choice", UNSET))

        def _parse_response_format(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        response_format = _parse_response_format(d.pop("response_format", UNSET))

        def _parse_reasoning_effort(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reasoning_effort = _parse_reasoning_effort(d.pop("reasoning_effort", UNSET))

        def _parse_verbosity(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        verbosity = _parse_verbosity(d.pop("verbosity", UNSET))

        def _parse_deployment_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deployment_name = _parse_deployment_name(d.pop("deployment_name", UNSET))

        run_params_map = cls(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stop_sequences=stop_sequences,
            top_p=top_p,
            top_k=top_k,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            echo=echo,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
            n=n,
            api_version=api_version,
            tools=tools,
            tool_choice=tool_choice,
            response_format=response_format,
            reasoning_effort=reasoning_effort,
            verbosity=verbosity,
            deployment_name=deployment_name,
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
