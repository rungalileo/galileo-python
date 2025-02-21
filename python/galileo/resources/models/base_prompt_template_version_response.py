from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.message import Message


T = TypeVar("T", bound="BasePromptTemplateVersionResponse")


@_attrs_define
class BasePromptTemplateVersionResponse:
    """Base response from API for a prompt template version.

    Attributes:
        id (str):
        template (Union[list['Message'], str]):
        version (int):
    """

    id: str
    template: Union[list["Message"], str]
    version: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        template: Union[list[dict[str, Any]], str]
        if isinstance(self.template, list):
            template = []
            for componentsschemas_messages_item_data in self.template:
                componentsschemas_messages_item = componentsschemas_messages_item_data.to_dict()
                template.append(componentsschemas_messages_item)

        else:
            template = self.template

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "template": template, "version": version})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.message import Message

        d = src_dict.copy()
        id = d.pop("id")

        def _parse_template(data: object) -> Union[list["Message"], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                template_type_1 = []
                _template_type_1 = data
                for componentsschemas_messages_item_data in _template_type_1:
                    componentsschemas_messages_item = Message.from_dict(componentsschemas_messages_item_data)

                    template_type_1.append(componentsschemas_messages_item)

                return template_type_1
            except:  # noqa: E722
                pass
            return cast(Union[list["Message"], str], data)

        template = _parse_template(d.pop("template"))

        version = d.pop("version")

        base_prompt_template_version_response = cls(id=id, template=template, version=version)

        base_prompt_template_version_response.additional_properties = d
        return base_prompt_template_version_response

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
