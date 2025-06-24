from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_prompt_template_version_settings import BasePromptTemplateVersionSettings
    from ..models.messages_list_item import MessagesListItem


T = TypeVar("T", bound="BasePromptTemplateVersion")


@_attrs_define
class BasePromptTemplateVersion:
    """
    Attributes:
        template (Union[list['MessagesListItem'], str]):
        output_type (Union[None, Unset, str]):
        raw (Union[Unset, bool]):  Default: False.
        settings (Union[Unset, BasePromptTemplateVersionSettings]):
        version (Union[None, Unset, int]):
    """

    template: Union[list["MessagesListItem"], str]
    output_type: Union[None, Unset, str] = UNSET
    raw: Union[Unset, bool] = False
    settings: Union[Unset, "BasePromptTemplateVersionSettings"] = UNSET
    version: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        template: Union[list[dict[str, Any]], str]
        if isinstance(self.template, list):
            template = []
            for componentsschemas_messages_item_data in self.template:
                componentsschemas_messages_item = componentsschemas_messages_item_data.to_dict()
                template.append(componentsschemas_messages_item)

        else:
            template = self.template

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
        field_dict.update({"template": template})
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
        from ..models.base_prompt_template_version_settings import BasePromptTemplateVersionSettings
        from ..models.messages_list_item import MessagesListItem

        d = dict(src_dict)

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

        def _parse_output_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        raw = d.pop("raw", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, BasePromptTemplateVersionSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = BasePromptTemplateVersionSettings.from_dict(_settings)

        def _parse_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        version = _parse_version(d.pop("version", UNSET))

        base_prompt_template_version = cls(
            template=template, output_type=output_type, raw=raw, settings=settings, version=version
        )

        base_prompt_template_version.additional_properties = d
        return base_prompt_template_version

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
