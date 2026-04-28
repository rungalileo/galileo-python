from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerExcludeSlmScorersFilter")


@_attrs_define
class ScorerExcludeSlmScorersFilter:
    """Internal filter: excludes scorers with model_type == slm while including
    scorers where model_type IS NULL. Auto-appended by the service layer.

    Attributes
    ----------
            name (Literal['exclude_slm_scorers'] | Unset):  Default: 'exclude_slm_scorers'.
    """

    name: Literal["exclude_slm_scorers"] | Unset = "exclude_slm_scorers"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = cast(Literal["exclude_slm_scorers"] | Unset, d.pop("name", UNSET))
        if name != "exclude_slm_scorers" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'exclude_slm_scorers', got '{name}'")

        scorer_exclude_slm_scorers_filter = cls(name=name)

        scorer_exclude_slm_scorers_filter.additional_properties = d
        return scorer_exclude_slm_scorers_filter

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
