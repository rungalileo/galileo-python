import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_prompt_template_version_response_settings import BasePromptTemplateVersionResponseSettings
    from ..models.messages_list_item import MessagesListItem


T = TypeVar("T", bound="BasePromptTemplateVersionResponse")


@_attrs_define
class BasePromptTemplateVersionResponse:
    """Base response from API for a prompt template version.

    Attributes:
        created_at (datetime.datetime):
        id (str):
        lines_added (int):
        lines_edited (int):
        lines_removed (int):
        model_changed (bool):
        settings (BasePromptTemplateVersionResponseSettings):
        settings_changed (bool):
        template (Union[list['MessagesListItem'], str]):
        updated_at (datetime.datetime):
        version (int):
        output_type (Union[None, Unset, str]):
        raw (Union[Unset, bool]):  Default: False.
    """

    created_at: datetime.datetime
    id: str
    lines_added: int
    lines_edited: int
    lines_removed: int
    model_changed: bool
    settings: "BasePromptTemplateVersionResponseSettings"
    settings_changed: bool
    template: Union[list["MessagesListItem"], str]
    updated_at: datetime.datetime
    version: int
    output_type: Union[None, Unset, str] = UNSET
    raw: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        lines_added = self.lines_added

        lines_edited = self.lines_edited

        lines_removed = self.lines_removed

        model_changed = self.model_changed

        settings = self.settings.to_dict()

        settings_changed = self.settings_changed

        template: Union[list[dict[str, Any]], str]
        if isinstance(self.template, list):
            template = []
            for componentsschemas_messages_item_data in self.template:
                componentsschemas_messages_item = componentsschemas_messages_item_data.to_dict()
                template.append(componentsschemas_messages_item)

        else:
            template = self.template

        updated_at = self.updated_at.isoformat()

        version = self.version

        output_type: Union[None, Unset, str]
        if isinstance(self.output_type, Unset):
            output_type = UNSET
        else:
            output_type = self.output_type

        raw = self.raw

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "id": id,
                "lines_added": lines_added,
                "lines_edited": lines_edited,
                "lines_removed": lines_removed,
                "model_changed": model_changed,
                "settings": settings,
                "settings_changed": settings_changed,
                "template": template,
                "updated_at": updated_at,
                "version": version,
            }
        )
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if raw is not UNSET:
            field_dict["raw"] = raw

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_prompt_template_version_response_settings import BasePromptTemplateVersionResponseSettings
        from ..models.messages_list_item import MessagesListItem

        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        lines_added = d.pop("lines_added")

        lines_edited = d.pop("lines_edited")

        lines_removed = d.pop("lines_removed")

        model_changed = d.pop("model_changed")

        settings = BasePromptTemplateVersionResponseSettings.from_dict(d.pop("settings"))

        settings_changed = d.pop("settings_changed")

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

        updated_at = isoparse(d.pop("updated_at"))

        version = d.pop("version")

        def _parse_output_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        raw = d.pop("raw", UNSET)

        base_prompt_template_version_response = cls(
            created_at=created_at,
            id=id,
            lines_added=lines_added,
            lines_edited=lines_edited,
            lines_removed=lines_removed,
            model_changed=model_changed,
            settings=settings,
            settings_changed=settings_changed,
            template=template,
            updated_at=updated_at,
            version=version,
            output_type=output_type,
            raw=raw,
        )

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
