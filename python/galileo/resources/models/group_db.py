import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.group_role import GroupRole
from ..models.group_visibility import GroupVisibility
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission


T = TypeVar("T", bound="GroupDB")


@_attrs_define
class GroupDB:
    """
    Attributes:
        created_at (datetime.datetime):
        id (str):
        name (str):
        size (int):
        description (Union[None, Unset, str]):
        permissions (Union[Unset, list['Permission']]):
        role (Union[GroupRole, None, Unset]): The role of the current user in the group.
        visibility (Union[Unset, GroupVisibility]):
    """

    created_at: datetime.datetime
    id: str
    name: str
    size: int
    description: Union[None, Unset, str] = UNSET
    permissions: Union[Unset, list["Permission"]] = UNSET
    role: Union[GroupRole, None, Unset] = UNSET
    visibility: Union[Unset, GroupVisibility] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        name = self.name

        size = self.size

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        permissions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        role: Union[None, Unset, str]
        if isinstance(self.role, Unset):
            role = UNSET
        elif isinstance(self.role, GroupRole):
            role = self.role.value
        else:
            role = self.role

        visibility: Union[Unset, str] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"created_at": created_at, "id": id, "name": name, "size": size})
        if description is not UNSET:
            field_dict["description"] = description
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if role is not UNSET:
            field_dict["role"] = role
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.permission import Permission

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        name = d.pop("name")

        size = d.pop("size")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        def _parse_role(data: object) -> Union[GroupRole, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_0 = GroupRole(data)

                return role_type_0
            except:  # noqa: E722
                pass
            return cast(Union[GroupRole, None, Unset], data)

        role = _parse_role(d.pop("role", UNSET))

        _visibility = d.pop("visibility", UNSET)
        visibility: Union[Unset, GroupVisibility]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = GroupVisibility(_visibility)

        group_db = cls(
            created_at=created_at,
            id=id,
            name=name,
            size=size,
            description=description,
            permissions=permissions,
            role=role,
            visibility=visibility,
        )

        group_db.additional_properties = d
        return group_db

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
