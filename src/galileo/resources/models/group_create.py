from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.group_visibility import GroupVisibility
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.group_member_create import GroupMemberCreate


T = TypeVar("T", bound="GroupCreate")


@_attrs_define
class GroupCreate:
    """
    Attributes:
        name (str):
        description (Union[None, Unset, str]):
        users (Union[Unset, list['GroupMemberCreate']]):
        visibility (Union[Unset, GroupVisibility]):
    """

    name: str
    description: Union[None, Unset, str] = UNSET
    users: Union[Unset, list["GroupMemberCreate"]] = UNSET
    visibility: Union[Unset, GroupVisibility] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        users: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        visibility: Union[Unset, str] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if description is not UNSET:
            field_dict["description"] = description
        if users is not UNSET:
            field_dict["users"] = users
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.group_member_create import GroupMemberCreate

        d = src_dict.copy()
        name = d.pop("name")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = GroupMemberCreate.from_dict(users_item_data)

            users.append(users_item)

        _visibility = d.pop("visibility", UNSET)
        visibility: Union[Unset, GroupVisibility]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = GroupVisibility(_visibility)

        group_create = cls(name=name, description=description, users=users, visibility=visibility)

        group_create.additional_properties = d
        return group_create

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
