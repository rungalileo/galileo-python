from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LlmMetrics")


@_attrs_define
class LlmMetrics:
    """
    Attributes:
        duration_ns (Union[None, Unset, int]): Duration of the trace or span in nanoseconds.  Displayed as 'Latency' in
            Galileo.
        num_input_tokens (Union[None, Unset, int]): Number of input tokens.
        num_output_tokens (Union[None, Unset, int]): Number of output tokens.
        num_total_tokens (Union[None, Unset, int]): Total number of tokens.
        time_to_first_token_ns (Union[None, Unset, int]): Time until the first token was generated in nanoseconds.
    """

    duration_ns: Union[None, Unset, int] = UNSET
    num_input_tokens: Union[None, Unset, int] = UNSET
    num_output_tokens: Union[None, Unset, int] = UNSET
    num_total_tokens: Union[None, Unset, int] = UNSET
    time_to_first_token_ns: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration_ns: Union[None, Unset, int]
        if isinstance(self.duration_ns, Unset):
            duration_ns = UNSET
        else:
            duration_ns = self.duration_ns

        num_input_tokens: Union[None, Unset, int]
        if isinstance(self.num_input_tokens, Unset):
            num_input_tokens = UNSET
        else:
            num_input_tokens = self.num_input_tokens

        num_output_tokens: Union[None, Unset, int]
        if isinstance(self.num_output_tokens, Unset):
            num_output_tokens = UNSET
        else:
            num_output_tokens = self.num_output_tokens

        num_total_tokens: Union[None, Unset, int]
        if isinstance(self.num_total_tokens, Unset):
            num_total_tokens = UNSET
        else:
            num_total_tokens = self.num_total_tokens

        time_to_first_token_ns: Union[None, Unset, int]
        if isinstance(self.time_to_first_token_ns, Unset):
            time_to_first_token_ns = UNSET
        else:
            time_to_first_token_ns = self.time_to_first_token_ns

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if duration_ns is not UNSET:
            field_dict["duration_ns"] = duration_ns
        if num_input_tokens is not UNSET:
            field_dict["num_input_tokens"] = num_input_tokens
        if num_output_tokens is not UNSET:
            field_dict["num_output_tokens"] = num_output_tokens
        if num_total_tokens is not UNSET:
            field_dict["num_total_tokens"] = num_total_tokens
        if time_to_first_token_ns is not UNSET:
            field_dict["time_to_first_token_ns"] = time_to_first_token_ns

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_duration_ns(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        duration_ns = _parse_duration_ns(d.pop("duration_ns", UNSET))

        def _parse_num_input_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_input_tokens = _parse_num_input_tokens(d.pop("num_input_tokens", UNSET))

        def _parse_num_output_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_output_tokens = _parse_num_output_tokens(d.pop("num_output_tokens", UNSET))

        def _parse_num_total_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_total_tokens = _parse_num_total_tokens(d.pop("num_total_tokens", UNSET))

        def _parse_time_to_first_token_ns(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        time_to_first_token_ns = _parse_time_to_first_token_ns(d.pop("time_to_first_token_ns", UNSET))

        llm_metrics = cls(
            duration_ns=duration_ns,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            num_total_tokens=num_total_tokens,
            time_to_first_token_ns=time_to_first_token_ns,
        )

        llm_metrics.additional_properties = d
        return llm_metrics

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
