from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.project_type import ProjectType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission
    from ..models.run_db_thin import RunDBThin


T = TypeVar("T", bound="ProjectDBThin")


@_attrs_define
class ProjectDBThin:
    """
    Attributes:
        id (str):
        created_by (str):
        runs (list[RunDBThin]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        permissions (list[Permission] | Unset):
        name (None | str | Unset):
        type_ (None | ProjectType | Unset):
        bookmark (bool | Unset):  Default: False.
    """

    id: str
    created_by: str
    runs: list[RunDBThin]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    permissions: list[Permission] | Unset = UNSET
    name: None | str | Unset = UNSET
    type_: None | ProjectType | Unset = UNSET
    bookmark: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_by = self.created_by

        runs = []
        for runs_item_data in self.runs:
            runs_item = runs_item_data.to_dict()
            runs.append(runs_item)

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        permissions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        type_: None | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        elif isinstance(self.type_, ProjectType):
            type_ = self.type_.value
        else:
            type_ = self.type_

        bookmark = self.bookmark

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "created_by": created_by, "runs": runs, "created_at": created_at, "updated_at": updated_at}
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if bookmark is not UNSET:
            field_dict["bookmark"] = bookmark

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission import Permission
        from ..models.run_db_thin import RunDBThin

        d = dict(src_dict)
        id = d.pop("id")

        created_by = d.pop("created_by")

        runs = []
        _runs = d.pop("runs")
        for runs_item_data in _runs:
            runs_item = RunDBThin.from_dict(runs_item_data)

            runs.append(runs_item)

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        _permissions = d.pop("permissions", UNSET)
        permissions: list[Permission] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = Permission.from_dict(permissions_item_data)

                permissions.append(permissions_item)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_type_(data: object) -> None | ProjectType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_0 = ProjectType(data)

                return type_type_0
            except:  # noqa: E722
                pass
            return cast(None | ProjectType | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

        bookmark = d.pop("bookmark", UNSET)

        project_db_thin = cls(
            id=id,
            created_by=created_by,
            runs=runs,
            created_at=created_at,
            updated_at=updated_at,
            permissions=permissions,
            name=name,
            type_=type_,
            bookmark=bookmark,
        )

        project_db_thin.additional_properties = d
        return project_db_thin

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
