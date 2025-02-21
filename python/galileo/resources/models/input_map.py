from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InputMap")


@_attrs_define
class InputMap:
    """
    Attributes:
        prompt (str):
        prefix (Union[Unset, str]):  Default: ''.
        suffix (Union[Unset, str]):  Default: ''.
    """

    prompt: str
    prefix: Union[Unset, str] = ""
    suffix: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        prefix = self.prefix

        suffix = self.suffix

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"prompt": prompt})
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if suffix is not UNSET:
            field_dict["suffix"] = suffix

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt")

        prefix = d.pop("prefix", UNSET)

        suffix = d.pop("suffix", UNSET)

        input_map = cls(prompt=prompt, prefix=prefix, suffix=suffix)

        input_map.additional_properties = d
        return input_map

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
