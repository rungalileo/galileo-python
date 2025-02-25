from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Changes")


@_attrs_define
class Changes:
    """
    Attributes:
        breaking (Union[Unset, list[str]]):
        features (Union[Unset, list[str]]):
        fixes (Union[Unset, list[str]]):
        miscellaneous (Union[Unset, list[str]]):
    """

    breaking: Union[Unset, list[str]] = UNSET
    features: Union[Unset, list[str]] = UNSET
    fixes: Union[Unset, list[str]] = UNSET
    miscellaneous: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        breaking: Union[Unset, list[str]] = UNSET
        if not isinstance(self.breaking, Unset):
            breaking = self.breaking

        features: Union[Unset, list[str]] = UNSET
        if not isinstance(self.features, Unset):
            features = self.features

        fixes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.fixes, Unset):
            fixes = self.fixes

        miscellaneous: Union[Unset, list[str]] = UNSET
        if not isinstance(self.miscellaneous, Unset):
            miscellaneous = self.miscellaneous

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if breaking is not UNSET:
            field_dict["breaking"] = breaking
        if features is not UNSET:
            field_dict["features"] = features
        if fixes is not UNSET:
            field_dict["fixes"] = fixes
        if miscellaneous is not UNSET:
            field_dict["miscellaneous"] = miscellaneous

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        breaking = cast(list[str], d.pop("breaking", UNSET))

        features = cast(list[str], d.pop("features", UNSET))

        fixes = cast(list[str], d.pop("fixes", UNSET))

        miscellaneous = cast(list[str], d.pop("miscellaneous", UNSET))

        changes = cls(breaking=breaking, features=features, fixes=fixes, miscellaneous=miscellaneous)

        changes.additional_properties = d
        return changes

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
