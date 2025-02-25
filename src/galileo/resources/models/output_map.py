from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OutputMap")


@_attrs_define
class OutputMap:
    """
    Attributes:
        response (str):
        completion_reason (Union[None, Unset, str]):
        input_token_count (Union[None, Unset, str]):
        output_token_count (Union[None, Unset, str]):
        token_count (Union[None, Unset, str]):
    """

    response: str
    completion_reason: Union[None, Unset, str] = UNSET
    input_token_count: Union[None, Unset, str] = UNSET
    output_token_count: Union[None, Unset, str] = UNSET
    token_count: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response = self.response

        completion_reason: Union[None, Unset, str]
        if isinstance(self.completion_reason, Unset):
            completion_reason = UNSET
        else:
            completion_reason = self.completion_reason

        input_token_count: Union[None, Unset, str]
        if isinstance(self.input_token_count, Unset):
            input_token_count = UNSET
        else:
            input_token_count = self.input_token_count

        output_token_count: Union[None, Unset, str]
        if isinstance(self.output_token_count, Unset):
            output_token_count = UNSET
        else:
            output_token_count = self.output_token_count

        token_count: Union[None, Unset, str]
        if isinstance(self.token_count, Unset):
            token_count = UNSET
        else:
            token_count = self.token_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"response": response})
        if completion_reason is not UNSET:
            field_dict["completion_reason"] = completion_reason
        if input_token_count is not UNSET:
            field_dict["input_token_count"] = input_token_count
        if output_token_count is not UNSET:
            field_dict["output_token_count"] = output_token_count
        if token_count is not UNSET:
            field_dict["token_count"] = token_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        response = d.pop("response")

        def _parse_completion_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        completion_reason = _parse_completion_reason(d.pop("completion_reason", UNSET))

        def _parse_input_token_count(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_token_count = _parse_input_token_count(d.pop("input_token_count", UNSET))

        def _parse_output_token_count(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_token_count = _parse_output_token_count(d.pop("output_token_count", UNSET))

        def _parse_token_count(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        token_count = _parse_token_count(d.pop("token_count", UNSET))

        output_map = cls(
            response=response,
            completion_reason=completion_reason,
            input_token_count=input_token_count,
            output_token_count=output_token_count,
            token_count=token_count,
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
