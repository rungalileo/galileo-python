from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.project_labels import ProjectLabels
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="ProjectItem")


@_attrs_define
class ProjectItem:
    """Represents a single project item for the UI list.

    Attributes:
        id (str):
        name (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        permissions (list[Permission] | Unset):
        bookmark (bool | Unset):  Default: False.
        num_logstreams (int | None | Unset): Count of runs with task_type=15
        num_experiments (int | None | Unset): Count of runs with task_type=16
        created_by_user (None | Unset | UserInfo):
        description (None | str | Unset):
        labels (list[ProjectLabels] | Unset): List of labels associated with the project.
    """

    id: str
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    permissions: list[Permission] | Unset = UNSET
    bookmark: bool | Unset = False
    num_logstreams: int | None | Unset = UNSET
    num_experiments: int | None | Unset = UNSET
    created_by_user: None | Unset | UserInfo = UNSET
    description: None | str | Unset = UNSET
    labels: list[ProjectLabels] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_info import UserInfo

        id = self.id

        name = self.name

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        permissions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        bookmark = self.bookmark

        num_logstreams: int | None | Unset
        if isinstance(self.num_logstreams, Unset):
            num_logstreams = UNSET
        else:
            num_logstreams = self.num_logstreams

        num_experiments: int | None | Unset
        if isinstance(self.num_experiments, Unset):
            num_experiments = UNSET
        else:
            num_experiments = self.num_experiments

        created_by_user: dict[str, Any] | None | Unset
        if isinstance(self.created_by_user, Unset):
            created_by_user = UNSET
        elif isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        labels: list[str] | Unset = UNSET
        if not isinstance(self.labels, Unset):
            labels = []
            for labels_item_data in self.labels:
                labels_item = labels_item_data.value
                labels.append(labels_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "name": name, "created_at": created_at, "updated_at": updated_at})
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if bookmark is not UNSET:
            field_dict["bookmark"] = bookmark
        if num_logstreams is not UNSET:
            field_dict["num_logstreams"] = num_logstreams
        if num_experiments is not UNSET:
            field_dict["num_experiments"] = num_experiments
        if created_by_user is not UNSET:
            field_dict["created_by_user"] = created_by_user
        if description is not UNSET:
            field_dict["description"] = description
        if labels is not UNSET:
            field_dict["labels"] = labels

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

        _permissions = d.pop("permissions", UNSET)
        permissions: list[Permission] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = Permission.from_dict(permissions_item_data)

                permissions.append(permissions_item)

        bookmark = d.pop("bookmark", UNSET)

        def _parse_num_logstreams(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_logstreams = _parse_num_logstreams(d.pop("num_logstreams", UNSET))

        def _parse_num_experiments(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_experiments = _parse_num_experiments(d.pop("num_experiments", UNSET))

        def _parse_created_by_user(data: object) -> None | Unset | UserInfo:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                created_by_user_type_0 = UserInfo.from_dict(data)

                return created_by_user_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | UserInfo, data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _labels = d.pop("labels", UNSET)
        labels: list[ProjectLabels] | Unset = UNSET
        if _labels is not UNSET:
            labels = []
            for labels_item_data in _labels:
                labels_item = ProjectLabels(labels_item_data)

                labels.append(labels_item)

        project_item = cls(
            id=id,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            permissions=permissions,
            bookmark=bookmark,
            num_logstreams=num_logstreams,
            num_experiments=num_experiments,
            created_by_user=created_by_user,
            description=description,
            labels=labels,
        )

        project_item.additional_properties = d
        return project_item

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
