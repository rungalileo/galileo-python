from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OutputMap")


@_attrs_define
class OutputMap:
    """
    Attributes
    ----------
        response (str):
        token_count (None | str | Unset):
        input_token_count (None | str | Unset):
        output_token_count (None | str | Unset):
        completion_reason (None | str | Unset):
    """

    response: str
    token_count: None | str | Unset = UNSET
    input_token_count: None | str | Unset = UNSET
    output_token_count: None | str | Unset = UNSET
    completion_reason: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response = self.response

        token_count: None | str | Unset
        token_count = UNSET if isinstance(self.token_count, Unset) else self.token_count

        input_token_count: None | str | Unset
        input_token_count = UNSET if isinstance(self.input_token_count, Unset) else self.input_token_count

        output_token_count: None | str | Unset
        output_token_count = UNSET if isinstance(self.output_token_count, Unset) else self.output_token_count

        completion_reason: None | str | Unset
        completion_reason = UNSET if isinstance(self.completion_reason, Unset) else self.completion_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"response": response})
        if token_count is not UNSET:
            field_dict["token_count"] = token_count
        if input_token_count is not UNSET:
            field_dict["input_token_count"] = input_token_count
        if output_token_count is not UNSET:
            field_dict["output_token_count"] = output_token_count
        if completion_reason is not UNSET:
            field_dict["completion_reason"] = completion_reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        response = d.pop("response")

        def _parse_token_count(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        token_count = _parse_token_count(d.pop("token_count", UNSET))

        def _parse_input_token_count(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        input_token_count = _parse_input_token_count(d.pop("input_token_count", UNSET))

        def _parse_output_token_count(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_token_count = _parse_output_token_count(d.pop("output_token_count", UNSET))

        def _parse_completion_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        completion_reason = _parse_completion_reason(d.pop("completion_reason", UNSET))

        output_map = cls(
            response=response,
            token_count=token_count,
            input_token_count=input_token_count,
            output_token_count=output_token_count,
            completion_reason=completion_reason,
        )

        output_map.additional_properties = d
        return output_map

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
