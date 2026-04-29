from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.messages_list_item import MessagesListItem
    from ..models.name import Name
    from ..models.prompt_run_settings import PromptRunSettings


T = TypeVar("T", bound="CreatePromptTemplateWithVersionRequestBody")


@_attrs_define
class CreatePromptTemplateWithVersionRequestBody:
    """Body to create a new prompt template with version.

    This is only used for parsing the body from the request.

    Attributes
    ----------
            template (Union[list['MessagesListItem'], str]):
            name (Union['Name', str]):
            raw (Union[Unset, bool]):  Default: False.
            version (Union[None, Unset, int]):
            settings (Union[Unset, PromptRunSettings]): Prompt run settings.
            output_type (Union[None, Unset, str]):
            hidden (Union[Unset, bool]):  Default: False.
    """

    template: Union[list["MessagesListItem"], str]
    name: Union["Name", str]
    raw: Union[Unset, bool] = False
    version: Union[None, Unset, int] = UNSET
    settings: Union[Unset, "PromptRunSettings"] = UNSET
    output_type: Union[None, Unset, str] = UNSET
    hidden: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.name import Name

        template: Union[list[dict[str, Any]], str]
        if isinstance(self.template, list):
            template = []
            for componentsschemas_messages_item_data in self.template:
                componentsschemas_messages_item = componentsschemas_messages_item_data.to_dict()
                template.append(componentsschemas_messages_item)

        else:
            template = self.template

        name: Union[dict[str, Any], str]
        name = self.name.to_dict() if isinstance(self.name, Name) else self.name

        raw = self.raw

        version: Union[None, Unset, int]
        version = UNSET if isinstance(self.version, Unset) else self.version

        settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        output_type: Union[None, Unset, str]
        output_type = UNSET if isinstance(self.output_type, Unset) else self.output_type

        hidden = self.hidden

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"template": template, "name": name})
        if raw is not UNSET:
            field_dict["raw"] = raw
        if version is not UNSET:
            field_dict["version"] = version
        if settings is not UNSET:
            field_dict["settings"] = settings
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if hidden is not UNSET:
            field_dict["hidden"] = hidden

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.messages_list_item import MessagesListItem
        from ..models.name import Name
        from ..models.prompt_run_settings import PromptRunSettings

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

        def _parse_name(data: object) -> Union["Name", str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Name.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["Name", str], data)

        name = _parse_name(d.pop("name"))

        raw = d.pop("raw", UNSET)

        def _parse_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        version = _parse_version(d.pop("version", UNSET))

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, PromptRunSettings]
        settings = UNSET if isinstance(_settings, Unset) else PromptRunSettings.from_dict(_settings)

        def _parse_output_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        hidden = d.pop("hidden", UNSET)

        create_prompt_template_with_version_request_body = cls(
            template=template,
            name=name,
            raw=raw,
            version=version,
            settings=settings,
            output_type=output_type,
            hidden=hidden,
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
