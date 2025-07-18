from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import cast, Union
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.messages_list_item import MessagesListItem
    from ..models.prompt_run_settings import PromptRunSettings
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="BasePromptTemplateVersionResponse")


@_attrs_define
class BasePromptTemplateVersionResponse:
    """Base response from API for a prompt template version.

    Attributes:
        content_changed (bool):
        created_at (datetime.datetime):
        created_by_user (Union['UserInfo', None]):
        id (str):
        model_changed (bool):
        settings (PromptRunSettings): Prompt run settings.
        settings_changed (bool):
        template (Union[list['MessagesListItem'], str]):
        updated_at (datetime.datetime):
        version (int):
        lines_added (Union[Unset, int]):  Default: 0.
        lines_edited (Union[Unset, int]):  Default: 0.
        lines_removed (Union[Unset, int]):  Default: 0.
        output_type (Union[None, Unset, str]):
        raw (Union[Unset, bool]):  Default: False.
    """

    content_changed: bool
    created_at: datetime.datetime
    created_by_user: Union["UserInfo", None]
    id: str
    model_changed: bool
    settings: "PromptRunSettings"
    settings_changed: bool
    template: Union[list["MessagesListItem"], str]
    updated_at: datetime.datetime
    version: int
    lines_added: Union[Unset, int] = 0
    lines_edited: Union[Unset, int] = 0
    lines_removed: Union[Unset, int] = 0
    output_type: Union[None, Unset, str] = UNSET
    raw: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.messages_list_item import MessagesListItem
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.user_info import UserInfo

        content_changed = self.content_changed

        created_at = self.created_at.isoformat()

        created_by_user: Union[None, dict[str, Any]]
        if isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        id = self.id

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

        lines_added = self.lines_added

        lines_edited = self.lines_edited

        lines_removed = self.lines_removed

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
                "content_changed": content_changed,
                "created_at": created_at,
                "created_by_user": created_by_user,
                "id": id,
                "model_changed": model_changed,
                "settings": settings,
                "settings_changed": settings_changed,
                "template": template,
                "updated_at": updated_at,
                "version": version,
            }
        )
        if lines_added is not UNSET:
            field_dict["lines_added"] = lines_added
        if lines_edited is not UNSET:
            field_dict["lines_edited"] = lines_edited
        if lines_removed is not UNSET:
            field_dict["lines_removed"] = lines_removed
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if raw is not UNSET:
            field_dict["raw"] = raw

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.messages_list_item import MessagesListItem
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        content_changed = d.pop("content_changed")

        created_at = isoparse(d.pop("created_at"))

        def _parse_created_by_user(data: object) -> Union["UserInfo", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                created_by_user_type_0 = UserInfo.from_dict(data)

                return created_by_user_type_0
            except:  # noqa: E722
                pass
            return cast(Union["UserInfo", None], data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user"))

        id = d.pop("id")

        model_changed = d.pop("model_changed")

        settings = PromptRunSettings.from_dict(d.pop("settings"))

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

        lines_added = d.pop("lines_added", UNSET)

        lines_edited = d.pop("lines_edited", UNSET)

        lines_removed = d.pop("lines_removed", UNSET)

        def _parse_output_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        raw = d.pop("raw", UNSET)

        base_prompt_template_version_response = cls(
            content_changed=content_changed,
            created_at=created_at,
            created_by_user=created_by_user,
            id=id,
            model_changed=model_changed,
            settings=settings,
            settings_changed=settings_changed,
            template=template,
            updated_at=updated_at,
            version=version,
            lines_added=lines_added,
            lines_edited=lines_edited,
            lines_removed=lines_removed,
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
