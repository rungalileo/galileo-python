from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunParamsMap")


@_attrs_define
class RunParamsMap:
    """Maps the internal settings parameters (left) to the serialized parameters (right) we want to send in the API
    requests.

        Attributes:
            model (None | str | Unset):
            temperature (None | str | Unset):
            max_tokens (None | str | Unset):
            stop_sequences (None | str | Unset):
            top_p (None | str | Unset):
            top_k (None | str | Unset):
            frequency_penalty (None | str | Unset):
            presence_penalty (None | str | Unset):
            echo (None | str | Unset):
            logprobs (None | str | Unset):
            top_logprobs (None | str | Unset):
            n (None | str | Unset):
            api_version (None | str | Unset):
            tools (None | str | Unset):
            tool_choice (None | str | Unset):
            response_format (None | str | Unset):
            reasoning_effort (None | str | Unset):
            verbosity (None | str | Unset):
            deployment_name (None | str | Unset):
    """

    model: None | str | Unset = UNSET
    temperature: None | str | Unset = UNSET
    max_tokens: None | str | Unset = UNSET
    stop_sequences: None | str | Unset = UNSET
    top_p: None | str | Unset = UNSET
    top_k: None | str | Unset = UNSET
    frequency_penalty: None | str | Unset = UNSET
    presence_penalty: None | str | Unset = UNSET
    echo: None | str | Unset = UNSET
    logprobs: None | str | Unset = UNSET
    top_logprobs: None | str | Unset = UNSET
    n: None | str | Unset = UNSET
    api_version: None | str | Unset = UNSET
    tools: None | str | Unset = UNSET
    tool_choice: None | str | Unset = UNSET
    response_format: None | str | Unset = UNSET
    reasoning_effort: None | str | Unset = UNSET
    verbosity: None | str | Unset = UNSET
    deployment_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model: None | str | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        temperature: None | str | Unset
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        max_tokens: None | str | Unset
        if isinstance(self.max_tokens, Unset):
            max_tokens = UNSET
        else:
            max_tokens = self.max_tokens

        stop_sequences: None | str | Unset
        if isinstance(self.stop_sequences, Unset):
            stop_sequences = UNSET
        else:
            stop_sequences = self.stop_sequences

        top_p: None | str | Unset
        if isinstance(self.top_p, Unset):
            top_p = UNSET
        else:
            top_p = self.top_p

        top_k: None | str | Unset
        if isinstance(self.top_k, Unset):
            top_k = UNSET
        else:
            top_k = self.top_k

        frequency_penalty: None | str | Unset
        if isinstance(self.frequency_penalty, Unset):
            frequency_penalty = UNSET
        else:
            frequency_penalty = self.frequency_penalty

        presence_penalty: None | str | Unset
        if isinstance(self.presence_penalty, Unset):
            presence_penalty = UNSET
        else:
            presence_penalty = self.presence_penalty

        echo: None | str | Unset
        if isinstance(self.echo, Unset):
            echo = UNSET
        else:
            echo = self.echo

        logprobs: None | str | Unset
        if isinstance(self.logprobs, Unset):
            logprobs = UNSET
        else:
            logprobs = self.logprobs

        top_logprobs: None | str | Unset
        if isinstance(self.top_logprobs, Unset):
            top_logprobs = UNSET
        else:
            top_logprobs = self.top_logprobs

        n: None | str | Unset
        if isinstance(self.n, Unset):
            n = UNSET
        else:
            n = self.n

        api_version: None | str | Unset
        if isinstance(self.api_version, Unset):
            api_version = UNSET
        else:
            api_version = self.api_version

        tools: None | str | Unset
        if isinstance(self.tools, Unset):
            tools = UNSET
        else:
            tools = self.tools

        tool_choice: None | str | Unset
        if isinstance(self.tool_choice, Unset):
            tool_choice = UNSET
        else:
            tool_choice = self.tool_choice

        response_format: None | str | Unset
        if isinstance(self.response_format, Unset):
            response_format = UNSET
        else:
            response_format = self.response_format

        reasoning_effort: None | str | Unset
        if isinstance(self.reasoning_effort, Unset):
            reasoning_effort = UNSET
        else:
            reasoning_effort = self.reasoning_effort

        verbosity: None | str | Unset
        if isinstance(self.verbosity, Unset):
            verbosity = UNSET
        else:
            verbosity = self.verbosity

        deployment_name: None | str | Unset
        if isinstance(self.deployment_name, Unset):
            deployment_name = UNSET
        else:
            deployment_name = self.deployment_name

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

        def _parse_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_temperature(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_max_tokens(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        max_tokens = _parse_max_tokens(d.pop("max_tokens", UNSET))

        def _parse_stop_sequences(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        stop_sequences = _parse_stop_sequences(d.pop("stop_sequences", UNSET))

        def _parse_top_p(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        top_p = _parse_top_p(d.pop("top_p", UNSET))

        def _parse_top_k(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        top_k = _parse_top_k(d.pop("top_k", UNSET))

        def _parse_frequency_penalty(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        frequency_penalty = _parse_frequency_penalty(d.pop("frequency_penalty", UNSET))

        def _parse_presence_penalty(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        presence_penalty = _parse_presence_penalty(d.pop("presence_penalty", UNSET))

        def _parse_echo(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        echo = _parse_echo(d.pop("echo", UNSET))

        def _parse_logprobs(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        logprobs = _parse_logprobs(d.pop("logprobs", UNSET))

        def _parse_top_logprobs(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        top_logprobs = _parse_top_logprobs(d.pop("top_logprobs", UNSET))

        def _parse_n(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        n = _parse_n(d.pop("n", UNSET))

        def _parse_api_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        api_version = _parse_api_version(d.pop("api_version", UNSET))

        def _parse_tools(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_tool_choice(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tool_choice = _parse_tool_choice(d.pop("tool_choice", UNSET))

        def _parse_response_format(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        response_format = _parse_response_format(d.pop("response_format", UNSET))

        def _parse_reasoning_effort(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reasoning_effort = _parse_reasoning_effort(d.pop("reasoning_effort", UNSET))

        def _parse_verbosity(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        verbosity = _parse_verbosity(d.pop("verbosity", UNSET))

        def _parse_deployment_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

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
