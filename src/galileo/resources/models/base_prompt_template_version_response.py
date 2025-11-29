import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.messages_list_item import MessagesListItem
    from ..models.prompt_run_settings import PromptRunSettings
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="BasePromptTemplateVersionResponse")


@_attrs_define
class BasePromptTemplateVersionResponse:
    """Base response from API for a prompt template version.

    Attributes
    ----------
        template (Union[list['MessagesListItem'], str]):
        version (int):
        settings (PromptRunSettings): Prompt run settings.
        id (str):
        model_changed (bool):
        settings_changed (bool):
        content_changed (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        created_by_user (Union['UserInfo', None]):
        raw (Union[Unset, bool]):  Default: False.
        output_type (Union[None, Unset, str]):
        lines_added (Union[Unset, int]):  Default: 0.
        lines_edited (Union[Unset, int]):  Default: 0.
        lines_removed (Union[Unset, int]):  Default: 0.
    """

    template: Union[list["MessagesListItem"], str]
    version: int
    settings: "PromptRunSettings"
    id: str
    model_changed: bool
    settings_changed: bool
    content_changed: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by_user: Union["UserInfo", None]
    raw: Union[Unset, bool] = False
    output_type: Union[None, Unset, str] = UNSET
    lines_added: Union[Unset, int] = 0
    lines_edited: Union[Unset, int] = 0
    lines_removed: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_info import UserInfo

        template: Union[list[dict[str, Any]], str]
        if isinstance(self.template, list):
            template = []
            for componentsschemas_messages_item_data in self.template:
                componentsschemas_messages_item = componentsschemas_messages_item_data.to_dict()
                template.append(componentsschemas_messages_item)

        else:
            template = self.template

        version = self.version

        settings = self.settings.to_dict()

        id = self.id

        model_changed = self.model_changed

        settings_changed = self.settings_changed

        content_changed = self.content_changed

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        created_by_user: Union[None, dict[str, Any]]
        if isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        raw = self.raw

        output_type: Union[None, Unset, str]
        output_type = UNSET if isinstance(self.output_type, Unset) else self.output_type

        lines_added = self.lines_added

        lines_edited = self.lines_edited

        lines_removed = self.lines_removed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "template": template,
                "version": version,
                "settings": settings,
                "id": id,
                "model_changed": model_changed,
                "settings_changed": settings_changed,
                "content_changed": content_changed,
                "created_at": created_at,
                "updated_at": updated_at,
                "created_by_user": created_by_user,
            }
        )
        if raw is not UNSET:
            field_dict["raw"] = raw
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if lines_added is not UNSET:
            field_dict["lines_added"] = lines_added
        if lines_edited is not UNSET:
            field_dict["lines_edited"] = lines_edited
        if lines_removed is not UNSET:
            field_dict["lines_removed"] = lines_removed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.messages_list_item import MessagesListItem
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.user_info import UserInfo

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

        version = d.pop("version")

        settings = PromptRunSettings.from_dict(d.pop("settings"))

        id = d.pop("id")

        model_changed = d.pop("model_changed")

        settings_changed = d.pop("settings_changed")

        content_changed = d.pop("content_changed")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_created_by_user(data: object) -> Union["UserInfo", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return UserInfo.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["UserInfo", None], data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user"))

        raw = d.pop("raw", UNSET)

        def _parse_output_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        lines_added = d.pop("lines_added", UNSET)

        lines_edited = d.pop("lines_edited", UNSET)

        lines_removed = d.pop("lines_removed", UNSET)

        base_prompt_template_version_response = cls(
            template=template,
            version=version,
            settings=settings,
            id=id,
            model_changed=model_changed,
            settings_changed=settings_changed,
            content_changed=content_changed,
            created_at=created_at,
            updated_at=updated_at,
            created_by_user=created_by_user,
            raw=raw,
            output_type=output_type,
            lines_added=lines_added,
            lines_edited=lines_edited,
            lines_removed=lines_removed,
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
