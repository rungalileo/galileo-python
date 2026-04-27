from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.messages_list_item_role import MessagesListItemRole

if TYPE_CHECKING:
    from ..models.file_content_part import FileContentPart
    from ..models.text_content_part import TextContentPart


T = TypeVar("T", bound="MessagesListItem")


@_attrs_define
class MessagesListItem:
    """
    Attributes:
        content (list[FileContentPart | TextContentPart] | str):
        role (MessagesListItemRole | str):
    """

    content: list[FileContentPart | TextContentPart] | str
    role: MessagesListItemRole | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.text_content_part import TextContentPart

        content: list[dict[str, Any]] | str
        if isinstance(self.content, list):
            content = []
            for content_type_1_item_data in self.content:
                content_type_1_item: dict[str, Any]
                if isinstance(content_type_1_item_data, TextContentPart):
                    content_type_1_item = content_type_1_item_data.to_dict()
                else:
                    content_type_1_item = content_type_1_item_data.to_dict()

                content.append(content_type_1_item)

        else:
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_content_part import FileContentPart
        from ..models.text_content_part import TextContentPart

        d = dict(src_dict)

        def _parse_content(data: object) -> list[FileContentPart | TextContentPart] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_1 = []
                _content_type_1 = data
                for content_type_1_item_data in _content_type_1:

                    def _parse_content_type_1_item(data: object) -> FileContentPart | TextContentPart:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            content_type_1_item_type_0 = TextContentPart.from_dict(data)

                            return content_type_1_item_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        content_type_1_item_type_1 = FileContentPart.from_dict(data)

                        return content_type_1_item_type_1

                    content_type_1_item = _parse_content_type_1_item(content_type_1_item_data)

                    content_type_1.append(content_type_1_item)

                return content_type_1
            except:  # noqa: E722
                pass
            return cast(list[FileContentPart | TextContentPart] | str, data)

        content = _parse_content(d.pop("content"))

        def _parse_role(data: object) -> MessagesListItemRole | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_1 = MessagesListItemRole(data)

                return role_type_1
            except:  # noqa: E722
                pass
            return cast(MessagesListItemRole | str, data)

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
