from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.group_db import GroupDB


T = TypeVar("T", bound="ListGroupsResponse")


@_attrs_define
class ListGroupsResponse:
    """
    Attributes:
        groups (list['GroupDB']):
        limit (Union[Unset, int]):  Default: 100.
        next_starting_token (Union[None, Unset, int]):
        paginated (Union[Unset, bool]):  Default: False.
        starting_token (Union[Unset, int]):  Default: 0.
    """

    groups: list["GroupDB"]
    limit: Union[Unset, int] = 100
    next_starting_token: Union[None, Unset, int] = UNSET
    paginated: Union[Unset, bool] = False
    starting_token: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()
            groups.append(groups_item)

        limit = self.limit

        next_starting_token: Union[None, Unset, int]
        if isinstance(self.next_starting_token, Unset):
            next_starting_token = UNSET
        else:
            next_starting_token = self.next_starting_token

        paginated = self.paginated

        starting_token = self.starting_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"groups": groups})
        if limit is not UNSET:
            field_dict["limit"] = limit
        if next_starting_token is not UNSET:
            field_dict["next_starting_token"] = next_starting_token
        if paginated is not UNSET:
            field_dict["paginated"] = paginated
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.group_db import GroupDB

        d = src_dict.copy()
        groups = []
        _groups = d.pop("groups")
        for groups_item_data in _groups:
            groups_item = GroupDB.from_dict(groups_item_data)

            groups.append(groups_item)

        limit = d.pop("limit", UNSET)

        def _parse_next_starting_token(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        next_starting_token = _parse_next_starting_token(d.pop("next_starting_token", UNSET))

        paginated = d.pop("paginated", UNSET)

        starting_token = d.pop("starting_token", UNSET)

        list_groups_response = cls(
            groups=groups,
            limit=limit,
            next_starting_token=next_starting_token,
            paginated=paginated,
            starting_token=starting_token,
        )

        list_groups_response.additional_properties = d
        return list_groups_response

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
