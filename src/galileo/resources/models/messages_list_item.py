from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.messages_list_item_role import MessagesListItemRole

T = TypeVar("T", bound="MessagesListItem")


@_attrs_define
class MessagesListItem:
    """
    Attributes:
        content (str):
        role (Union[MessagesListItemRole, str]):
    """

    content: str
    role: Union[MessagesListItemRole, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        role: str
        if isinstance(self.role, MessagesListItemRole):
            role = self.role.value
        else:
            role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"content": content, "role": role})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        content = d.pop("content")

        def _parse_role(data: object) -> Union[MessagesListItemRole, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_1 = MessagesListItemRole(data)

                return role_type_1
            except:  # noqa: E722
                pass
            return cast(Union[MessagesListItemRole, str], data)

        role = _parse_role(d.pop("role"))

        messages_list_item = cls(content=content, role=role)

        messages_list_item.additional_properties = d
        return messages_list_item

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
