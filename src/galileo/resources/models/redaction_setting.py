from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.redaction_filter import RedactionFilter


T = TypeVar("T", bound="RedactionSetting")


@_attrs_define
class RedactionSetting:
    """Redaction setting for RBAC-based content filtering.

    Attributes:
        settings_key (Literal['redaction'] | Unset):  Default: 'redaction'.
        filters (list[RedactionFilter] | Unset):
    """

    settings_key: Literal["redaction"] | Unset = "redaction"
    filters: list[RedactionFilter] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        settings_key = self.settings_key

        filters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if settings_key is not UNSET:
            field_dict["settings_key"] = settings_key
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.redaction_filter import RedactionFilter

        d = dict(src_dict)
        settings_key = cast(Literal["redaction"] | Unset, d.pop("settings_key", UNSET))
        if settings_key != "redaction" and not isinstance(settings_key, Unset):
            raise ValueError(f"settings_key must match const 'redaction', got '{settings_key}'")

        _filters = d.pop("filters", UNSET)
        filters: list[RedactionFilter] | Unset = UNSET
        if _filters is not UNSET:
            filters = []
            for filters_item_data in _filters:
                filters_item = RedactionFilter.from_dict(filters_item_data)

                filters.append(filters_item)

        redaction_setting = cls(settings_key=settings_key, filters=filters)

        redaction_setting.additional_properties = d
        return redaction_setting

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
