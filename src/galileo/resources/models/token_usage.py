from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenUsage")


@_attrs_define
class TokenUsage:
    """Token usage information for insights generation.

    Attributes:
        input_tokens (int | None | Unset):
        output_tokens (int | None | Unset):
        cache_read_input_tokens (int | None | Unset):
        cache_creation_input_tokens (int | None | Unset):
    """

    input_tokens: int | None | Unset = UNSET
    output_tokens: int | None | Unset = UNSET
    cache_read_input_tokens: int | None | Unset = UNSET
    cache_creation_input_tokens: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_tokens: int | None | Unset
        if isinstance(self.input_tokens, Unset):
            input_tokens = UNSET
        else:
            input_tokens = self.input_tokens

        output_tokens: int | None | Unset
        if isinstance(self.output_tokens, Unset):
            output_tokens = UNSET
        else:
            output_tokens = self.output_tokens

        cache_read_input_tokens: int | None | Unset
        if isinstance(self.cache_read_input_tokens, Unset):
            cache_read_input_tokens = UNSET
        else:
            cache_read_input_tokens = self.cache_read_input_tokens

        cache_creation_input_tokens: int | None | Unset
        if isinstance(self.cache_creation_input_tokens, Unset):
            cache_creation_input_tokens = UNSET
        else:
            cache_creation_input_tokens = self.cache_creation_input_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if cache_read_input_tokens is not UNSET:
            field_dict["cache_read_input_tokens"] = cache_read_input_tokens
        if cache_creation_input_tokens is not UNSET:
            field_dict["cache_creation_input_tokens"] = cache_creation_input_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_input_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        input_tokens = _parse_input_tokens(d.pop("input_tokens", UNSET))

        def _parse_output_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        output_tokens = _parse_output_tokens(d.pop("output_tokens", UNSET))

        def _parse_cache_read_input_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cache_read_input_tokens = _parse_cache_read_input_tokens(d.pop("cache_read_input_tokens", UNSET))

        def _parse_cache_creation_input_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cache_creation_input_tokens = _parse_cache_creation_input_tokens(d.pop("cache_creation_input_tokens", UNSET))

        token_usage = cls(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_read_input_tokens=cache_read_input_tokens,
            cache_creation_input_tokens=cache_creation_input_tokens,
        )

        token_usage.additional_properties = d
        return token_usage

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
