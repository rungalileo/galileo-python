from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerExcludeMultimodalScorersFilter")


@_attrs_define
class ScorerExcludeMultimodalScorersFilter:
    """Internal filter: excludes multimodal scorers (non-empty multimodal_capabilities).

    Auto-appended by the service layer when the `multimodal` feature flag is disabled.

    Attributes
    ----------
            name (Union[Literal['exclude_multimodal_scorers'], Unset]):  Default: 'exclude_multimodal_scorers'.
    """

    name: Literal["exclude_multimodal_scorers"] | Unset = "exclude_multimodal_scorers"
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
        name = cast(Literal["exclude_multimodal_scorers"] | Unset, d.pop("name", UNSET))
        if name != "exclude_multimodal_scorers" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'exclude_multimodal_scorers', got '{name}'")

        scorer_exclude_multimodal_scorers_filter = cls(name=name)

        scorer_exclude_multimodal_scorers_filter.additional_properties = d
        return scorer_exclude_multimodal_scorers_filter

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
