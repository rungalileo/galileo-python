from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_prompt_template_with_version_request_body_settings import (
        CreatePromptTemplateWithVersionRequestBodySettings,
    )
    from ..models.messages_list_item import MessagesListItem


T = TypeVar("T", bound="CreatePromptTemplateWithVersionRequestBody")


@_attrs_define
class CreatePromptTemplateWithVersionRequestBody:
    """Body to create a new prompt template with version.

    This is only used for parsing the body from the request.

        Attributes:
            name (str):
            template (Union[list['MessagesListItem'], str]):
            hidden (Union[Unset, bool]):  Default: False.
            output_type (Union[None, Unset, str]):
            raw (Union[Unset, bool]):  Default: False.
            settings (Union[Unset, CreatePromptTemplateWithVersionRequestBodySettings]):
            version (Union[None, Unset, int]):
    """

    name: str
    template: Union[list["MessagesListItem"], str]
    hidden: Union[Unset, bool] = False
    output_type: Union[None, Unset, str] = UNSET
    raw: Union[Unset, bool] = False
    settings: Union[Unset, "CreatePromptTemplateWithVersionRequestBodySettings"] = UNSET
    version: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        template: Union[list[dict[str, Any]], str]
        if isinstance(self.template, list):
            template = []
            for componentsschemas_messages_item_data in self.template:
                componentsschemas_messages_item = componentsschemas_messages_item_data.to_dict()
                template.append(componentsschemas_messages_item)

        else:
            template = self.template

        hidden = self.hidden

        output_type: Union[None, Unset, str]
        if isinstance(self.output_type, Unset):
            output_type = UNSET
        else:
            output_type = self.output_type

        raw = self.raw

        settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        version: Union[None, Unset, int]
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "template": template})
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if raw is not UNSET:
            field_dict["raw"] = raw
        if settings is not UNSET:
            field_dict["settings"] = settings
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_prompt_template_with_version_request_body_settings import (
            CreatePromptTemplateWithVersionRequestBodySettings,
        )
        from ..models.messages_list_item import MessagesListItem

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_template(data: object) -> Union[list["MessagesListItem"], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                template_type_1 = []
                _template_type_1 = data
                for componentsschemas_messages_item_data in _template_type_1:
                    componentsschemas_messages_item = MessagesListItem.from_dict(componentsschemas_messages_item_data)

                    template_type_1.append(componentsschemas_messages_item)

                return template_type_1
            except:  # noqa: E722
                pass
            return cast(Union[list["MessagesListItem"], str], data)

        template = _parse_template(d.pop("template"))

        hidden = d.pop("hidden", UNSET)

        def _parse_output_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        raw = d.pop("raw", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, CreatePromptTemplateWithVersionRequestBodySettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = CreatePromptTemplateWithVersionRequestBodySettings.from_dict(_settings)

        def _parse_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        version = _parse_version(d.pop("version", UNSET))

        create_prompt_template_with_version_request_body = cls(
            name=name,
            template=template,
            hidden=hidden,
            output_type=output_type,
            raw=raw,
            settings=settings,
            version=version,
        )

        create_prompt_template_with_version_request_body.additional_properties = d
        return create_prompt_template_with_version_request_body

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
