from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatePlaygroundPromptRequest")


@_attrs_define
class CreatePlaygroundPromptRequest:
    """
    Attributes:
        playground_prompt_id (None | str | Unset): If provided, the new prompt will be a copy of the existing one.
    """

    playground_prompt_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        playground_prompt_id: None | str | Unset
        if isinstance(self.playground_prompt_id, Unset):
            playground_prompt_id = UNSET
        else:
            playground_prompt_id = self.playground_prompt_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if playground_prompt_id is not UNSET:
            field_dict["playground_prompt_id"] = playground_prompt_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_playground_prompt_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        playground_prompt_id = _parse_playground_prompt_id(d.pop("playground_prompt_id", UNSET))

        create_playground_prompt_request = cls(playground_prompt_id=playground_prompt_id)

        create_playground_prompt_request.additional_properties = d
        return create_playground_prompt_request

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
