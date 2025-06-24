import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
        id (str):
        name (str):
        updated_at (datetime.datetime):
        bookmark (Union[Unset, bool]):  Default: False.
        created_by_user (Union['UserInfo', None, Unset]):
        num_experiments (Union[None, Unset, int]): Count of runs with task_type=16
        num_logstreams (Union[None, Unset, int]): Count of runs with task_type=15
        permissions (Union[Unset, list['Permission']]):
    """

    created_at: datetime.datetime
    id: str
    name: str
    updated_at: datetime.datetime
    bookmark: Union[Unset, bool] = False
    created_by_user: Union["UserInfo", None, Unset] = UNSET
    num_experiments: Union[None, Unset, int] = UNSET
    num_logstreams: Union[None, Unset, int] = UNSET
    permissions: Union[Unset, list["Permission"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_info import UserInfo

        created_at = self.created_at.isoformat()

        id = self.id

        name = self.name

        updated_at = self.updated_at.isoformat()

        bookmark = self.bookmark

        created_by_user: Union[None, Unset, dict[str, Any]]
        if isinstance(self.created_by_user, Unset):
            created_by_user = UNSET
        elif isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        num_experiments: Union[None, Unset, int]
        if isinstance(self.num_experiments, Unset):
            num_experiments = UNSET
        else:
            num_experiments = self.num_experiments

        num_logstreams: Union[None, Unset, int]
        if isinstance(self.num_logstreams, Unset):
            num_logstreams = UNSET
        else:
            num_logstreams = self.num_logstreams

        permissions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"created_at": created_at, "id": id, "name": name, "updated_at": updated_at})
        if bookmark is not UNSET:
            field_dict["bookmark"] = bookmark
        if created_by_user is not UNSET:
            field_dict["created_by_user"] = created_by_user
        if num_experiments is not UNSET:
            field_dict["num_experiments"] = num_experiments
        if num_logstreams is not UNSET:
            field_dict["num_logstreams"] = num_logstreams
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission import Permission
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        name = d.pop("name")

        updated_at = isoparse(d.pop("updated_at"))

        bookmark = d.pop("bookmark", UNSET)

        def _parse_created_by_user(data: object) -> Union["UserInfo", None, Unset]:
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
            return cast(Union["UserInfo", None, Unset], data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user", UNSET))

        def _parse_num_experiments(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_experiments = _parse_num_experiments(d.pop("num_experiments", UNSET))

        def _parse_num_logstreams(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_logstreams = _parse_num_logstreams(d.pop("num_logstreams", UNSET))

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        project_item = cls(
            created_at=created_at,
            id=id,
            name=name,
            updated_at=updated_at,
            bookmark=bookmark,
            created_by_user=created_by_user,
            num_experiments=num_experiments,
            num_logstreams=num_logstreams,
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
