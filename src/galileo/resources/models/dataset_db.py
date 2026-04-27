from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="DatasetDB")


@_attrs_define
class DatasetDB:
    """
    Attributes:
        id (str):
        name (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        project_count (int):
        num_rows (int | None):
        column_names (list[str] | None):
        created_by_user (None | UserInfo):
        current_version_index (int):
        draft (bool):
        permissions (list[Permission] | Unset):
    """

    id: str
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    project_count: int
    num_rows: int | None
    column_names: list[str] | None
    created_by_user: None | UserInfo
    current_version_index: int
    draft: bool
    permissions: list[Permission] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_info import UserInfo

        id = self.id

        name = self.name

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        project_count = self.project_count

        num_rows: int | None
        num_rows = self.num_rows

        column_names: list[str] | None
        if isinstance(self.column_names, list):
            column_names = self.column_names

        else:
            column_names = self.column_names

        created_by_user: dict[str, Any] | None
        if isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        current_version_index = self.current_version_index

        draft = self.draft

        permissions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "created_at": created_at,
                "updated_at": updated_at,
                "project_count": project_count,
                "num_rows": num_rows,
                "column_names": column_names,
                "created_by_user": created_by_user,
                "current_version_index": current_version_index,
                "draft": draft,
            }
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission import Permission
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        project_count = d.pop("project_count")

        def _parse_num_rows(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        num_rows = _parse_num_rows(d.pop("num_rows"))

        def _parse_column_names(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                column_names_type_0 = cast(list[str], data)

                return column_names_type_0
            except:  # noqa: E722
                pass
            return cast(list[str] | None, data)

        column_names = _parse_column_names(d.pop("column_names"))

        def _parse_created_by_user(data: object) -> None | UserInfo:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                created_by_user_type_0 = UserInfo.from_dict(data)

                return created_by_user_type_0
            except:  # noqa: E722
                pass
            return cast(None | UserInfo, data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user"))

        current_version_index = d.pop("current_version_index")

        draft = d.pop("draft")

        _permissions = d.pop("permissions", UNSET)
        permissions: list[Permission] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = Permission.from_dict(permissions_item_data)

                permissions.append(permissions_item)

        dataset_db = cls(
            id=id,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            project_count=project_count,
            num_rows=num_rows,
            column_names=column_names,
            created_by_user=created_by_user,
            current_version_index=current_version_index,
            draft=draft,
            permissions=permissions,
        )

        dataset_db.additional_properties = d
        return dataset_db

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
