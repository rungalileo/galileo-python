from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.group_visibility import GroupVisibility

T = TypeVar("T", bound="GroupUpdate")


@_attrs_define
class GroupUpdate:
    """
    Attributes:
        description (Union[None, str]):
        name (str):
        visibility (GroupVisibility):
    """

    description: Union[None, str]
    name: str
    visibility: GroupVisibility
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description: Union[None, str]
        description = self.description

        name = self.name

        visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"description": description, "name": name, "visibility": visibility})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        name = d.pop("name")

        visibility = GroupVisibility(d.pop("visibility"))

        group_update = cls(description=description, name=name, visibility=visibility)

        group_update.additional_properties = d
        return group_update

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
