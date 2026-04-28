from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.name import Name


T = TypeVar("T", bound="UpdatePromptTemplateRequest")


@_attrs_define
class UpdatePromptTemplateRequest:
    """
    Attributes
    ----------
        name (Name | None | str | Unset):
    """

    name: Name | None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.name import Name

        name: dict[str, Any] | None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, Name):
            name = self.name.to_dict()
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.name import Name

        d = dict(src_dict)

        def _parse_name(data: object) -> Name | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Name.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Name | None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        update_prompt_template_request = cls(name=name)

        update_prompt_template_request.additional_properties = d
        return update_prompt_template_request

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
