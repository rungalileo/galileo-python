import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="ProjectItem")


@_attrs_define
class ProjectItem:
    """Represents a single project item for the UI list.

    Attributes:
        created_at (datetime.datetime):
        created_by_user (UserInfo): A user's basic information, used for display purposes.
        id (str):
        name (str):
        num_experiments (int): Count of runs with task_type=16
        num_logstreams (int): Count of runs with task_type=15
        updated_at (datetime.datetime):
        bookmark (Union[Unset, bool]):  Default: False.
        permissions (Union[Unset, list['Permission']]):
    """

    created_at: datetime.datetime
    created_by_user: "UserInfo"
    id: str
    name: str
    num_experiments: int
    num_logstreams: int
    updated_at: datetime.datetime
    bookmark: Union[Unset, bool] = False
    permissions: Union[Unset, list["Permission"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by_user = self.created_by_user.to_dict()

        id = self.id

        name = self.name

        num_experiments = self.num_experiments

        num_logstreams = self.num_logstreams

        updated_at = self.updated_at.isoformat()

        bookmark = self.bookmark

        permissions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by_user": created_by_user,
                "id": id,
                "name": name,
                "num_experiments": num_experiments,
                "num_logstreams": num_logstreams,
                "updated_at": updated_at,
            }
        )
        if bookmark is not UNSET:
            field_dict["bookmark"] = bookmark
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.permission import Permission
        from ..models.user_info import UserInfo

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        created_by_user = UserInfo.from_dict(d.pop("created_by_user"))

        id = d.pop("id")

        name = d.pop("name")

        num_experiments = d.pop("num_experiments")

        num_logstreams = d.pop("num_logstreams")

        updated_at = isoparse(d.pop("updated_at"))

        bookmark = d.pop("bookmark", UNSET)

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        project_item = cls(
            created_at=created_at,
            created_by_user=created_by_user,
            id=id,
            name=name,
            num_experiments=num_experiments,
            num_logstreams=num_logstreams,
            updated_at=updated_at,
            bookmark=bookmark,
            permissions=permissions,
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
