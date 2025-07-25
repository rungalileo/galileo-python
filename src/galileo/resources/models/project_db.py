import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.project_labels import ProjectLabels
from ..models.project_type import ProjectType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission
    from ..models.run_db import RunDB
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="ProjectDB")


@_attrs_define
class ProjectDB:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by (str):
        created_by_user (UserInfo): A user's basic information, used for display purposes.
        id (str):
        runs (list['RunDB']):
        updated_at (datetime.datetime):
        bookmark (Union[Unset, bool]):  Default: False.
        description (Union[None, Unset, str]):
        labels (Union[Unset, list[ProjectLabels]]):
        name (Union[None, Unset, str]):
        permissions (Union[Unset, list['Permission']]):
        type_ (Union[None, ProjectType, Unset]):
    """

    created_at: datetime.datetime
    created_by: str
    created_by_user: "UserInfo"
    id: str
    runs: list["RunDB"]
    updated_at: datetime.datetime
    bookmark: Union[Unset, bool] = False
    description: Union[None, Unset, str] = UNSET
    labels: Union[Unset, list[ProjectLabels]] = UNSET
    name: Union[None, Unset, str] = UNSET
    permissions: Union[Unset, list["Permission"]] = UNSET
    type_: Union[None, ProjectType, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        created_by_user = self.created_by_user.to_dict()

        id = self.id

        runs = []
        for runs_item_data in self.runs:
            runs_item = runs_item_data.to_dict()
            runs.append(runs_item)

        updated_at = self.updated_at.isoformat()

        bookmark = self.bookmark

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        labels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = []
            for labels_item_data in self.labels:
                labels_item = labels_item_data.value
                labels.append(labels_item)

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        permissions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        elif isinstance(self.type_, ProjectType):
            type_ = self.type_.value
        else:
            type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by": created_by,
                "created_by_user": created_by_user,
                "id": id,
                "runs": runs,
                "updated_at": updated_at,
            }
        )
        if bookmark is not UNSET:
            field_dict["bookmark"] = bookmark
        if description is not UNSET:
            field_dict["description"] = description
        if labels is not UNSET:
            field_dict["labels"] = labels
        if name is not UNSET:
            field_dict["name"] = name
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission import Permission
        from ..models.run_db import RunDB
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        created_by_user = UserInfo.from_dict(d.pop("created_by_user"))

        id = d.pop("id")

        runs = []
        _runs = d.pop("runs")
        for runs_item_data in _runs:
            runs_item = RunDB.from_dict(runs_item_data)

            runs.append(runs_item)

        updated_at = isoparse(d.pop("updated_at"))

        bookmark = d.pop("bookmark", UNSET)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        labels = []
        _labels = d.pop("labels", UNSET)
        for labels_item_data in _labels or []:
            labels_item = ProjectLabels(labels_item_data)

            labels.append(labels_item)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        def _parse_type_(data: object) -> Union[None, ProjectType, Unset]:
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
            return cast(Union[None, ProjectType, Unset], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        project_db = cls(
            created_at=created_at,
            created_by=created_by,
            created_by_user=created_by_user,
            id=id,
            runs=runs,
            updated_at=updated_at,
            bookmark=bookmark,
            description=description,
            labels=labels,
            name=name,
            permissions=permissions,
            type_=type_,
        )

        project_db.additional_properties = d
        return project_db

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
