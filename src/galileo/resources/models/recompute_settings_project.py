from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecomputeSettingsProject")


@_attrs_define
class RecomputeSettingsProject:
    """
    Attributes:
        mode (Union[Literal['project'], Unset]):  Default: 'project'.
    """

    mode: Union[Literal["project"], Unset] = "project"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        mode = cast(Union[Literal["project"], Unset], d.pop("mode", UNSET))
        if mode != "project" and not isinstance(mode, Unset):
            raise ValueError(f"mode must match const 'project', got '{mode}'")

        recompute_settings_project = cls(mode=mode)

        recompute_settings_project.additional_properties = d
        return recompute_settings_project

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
