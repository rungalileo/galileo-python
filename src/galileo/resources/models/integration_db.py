from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.integration_name import IntegrationName
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission


T = TypeVar("T", bound="IntegrationDB")


@_attrs_define
class IntegrationDB:
    """
    Attributes
    ----------
        id (str):
        name (IntegrationName):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        created_by (str):
        permissions (list[Permission] | Unset):
        is_selected (bool | Unset):  Default: False.
        is_disabled (bool | Unset):  Default: False.
    """

    id: str
    name: IntegrationName
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: str
    permissions: list[Permission] | Unset = UNSET
    is_selected: bool | Unset = False
    is_disabled: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        created_by = self.created_by

        permissions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        is_selected = self.is_selected

        is_disabled = self.is_disabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "name": name, "created_at": created_at, "updated_at": updated_at, "created_by": created_by}
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if is_selected is not UNSET:
            field_dict["is_selected"] = is_selected
        if is_disabled is not UNSET:
            field_dict["is_disabled"] = is_disabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission import Permission

        d = dict(src_dict)
        id = d.pop("id")

        name = IntegrationName(d.pop("name"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        created_by = d.pop("created_by")

        _permissions = d.pop("permissions", UNSET)
        permissions: list[Permission] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = Permission.from_dict(permissions_item_data)

                permissions.append(permissions_item)

        is_selected = d.pop("is_selected", UNSET)

        is_disabled = d.pop("is_disabled", UNSET)

        integration_db = cls(
            id=id,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            permissions=permissions,
            is_selected=is_selected,
            is_disabled=is_disabled,
        )

        integration_db.additional_properties = d
        return integration_db

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
