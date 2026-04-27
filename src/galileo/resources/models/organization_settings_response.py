from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.redaction_setting import RedactionSetting
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="OrganizationSettingsResponse")


@_attrs_define
class OrganizationSettingsResponse:
    """Response schema for an organization setting.

    Attributes:
        value (RedactionSetting): Redaction setting for RBAC-based content filtering.
        updated_at (datetime.datetime):
        updated_by (None | UUID):
        updated_by_user (None | UserInfo):
    """

    value: RedactionSetting
    updated_at: datetime.datetime
    updated_by: None | UUID
    updated_by_user: None | UserInfo
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_info import UserInfo

        value = self.value.to_dict()

        updated_at = self.updated_at.isoformat()

        updated_by: None | str
        if isinstance(self.updated_by, UUID):
            updated_by = str(self.updated_by)
        else:
            updated_by = self.updated_by

        updated_by_user: dict[str, Any] | None
        if isinstance(self.updated_by_user, UserInfo):
            updated_by_user = self.updated_by_user.to_dict()
        else:
            updated_by_user = self.updated_by_user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"value": value, "updated_at": updated_at, "updated_by": updated_by, "updated_by_user": updated_by_user}
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.redaction_setting import RedactionSetting
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        value = RedactionSetting.from_dict(d.pop("value"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_updated_by(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_by_type_0 = UUID(data)

                return updated_by_type_0
            except:  # noqa: E722
                pass
            return cast(None | UUID, data)

        updated_by = _parse_updated_by(d.pop("updated_by"))

        def _parse_updated_by_user(data: object) -> None | UserInfo:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                updated_by_user_type_0 = UserInfo.from_dict(data)

                return updated_by_user_type_0
            except:  # noqa: E722
                pass
            return cast(None | UserInfo, data)

        updated_by_user = _parse_updated_by_user(d.pop("updated_by_user"))

        organization_settings_response = cls(
            value=value, updated_at=updated_at, updated_by=updated_by, updated_by_user=updated_by_user
        )

        organization_settings_response.additional_properties = d
        return organization_settings_response

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
