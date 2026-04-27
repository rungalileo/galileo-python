from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_queue_response_num_logs_annotated_type_0 import (
        AnnotationQueueResponseNumLogsAnnotatedType0,
    )
    from ..models.annotation_queue_response_progress_type_0 import AnnotationQueueResponseProgressType0
    from ..models.annotation_template_db import AnnotationTemplateDB
    from ..models.permission import Permission
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="AnnotationQueueResponse")


@_attrs_define
class AnnotationQueueResponse:
    """
    Attributes:
        id (str):
        name (str):
        description (None | str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        created_by_user (None | UserInfo):
        permissions (list[Permission] | Unset):
        num_log_records (int | Unset):  Default: 0.
        num_annotators (int | Unset):  Default: 0.
        num_users (int | Unset):  Default: 0.
        num_templates (int | Unset):  Default: 0.
        num_logs_annotated (AnnotationQueueResponseNumLogsAnnotatedType0 | None | Unset):
        progress (AnnotationQueueResponseProgressType0 | None | Unset):
        overall_progress (float | None | Unset):
        templates (list[AnnotationTemplateDB] | Unset):
    """

    id: str
    name: str
    description: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by_user: None | UserInfo
    permissions: list[Permission] | Unset = UNSET
    num_log_records: int | Unset = 0
    num_annotators: int | Unset = 0
    num_users: int | Unset = 0
    num_templates: int | Unset = 0
    num_logs_annotated: AnnotationQueueResponseNumLogsAnnotatedType0 | None | Unset = UNSET
    progress: AnnotationQueueResponseProgressType0 | None | Unset = UNSET
    overall_progress: float | None | Unset = UNSET
    templates: list[AnnotationTemplateDB] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.annotation_queue_response_num_logs_annotated_type_0 import (
            AnnotationQueueResponseNumLogsAnnotatedType0,
        )
        from ..models.annotation_queue_response_progress_type_0 import AnnotationQueueResponseProgressType0
        from ..models.user_info import UserInfo

        id = self.id

        name = self.name

        description: None | str
        description = self.description

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        created_by_user: dict[str, Any] | None
        if isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        permissions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        num_log_records = self.num_log_records

        num_annotators = self.num_annotators

        num_users = self.num_users

        num_templates = self.num_templates

        num_logs_annotated: dict[str, Any] | None | Unset
        if isinstance(self.num_logs_annotated, Unset):
            num_logs_annotated = UNSET
        elif isinstance(self.num_logs_annotated, AnnotationQueueResponseNumLogsAnnotatedType0):
            num_logs_annotated = self.num_logs_annotated.to_dict()
        else:
            num_logs_annotated = self.num_logs_annotated

        progress: dict[str, Any] | None | Unset
        if isinstance(self.progress, Unset):
            progress = UNSET
        elif isinstance(self.progress, AnnotationQueueResponseProgressType0):
            progress = self.progress.to_dict()
        else:
            progress = self.progress

        overall_progress: float | None | Unset
        if isinstance(self.overall_progress, Unset):
            overall_progress = UNSET
        else:
            overall_progress = self.overall_progress

        templates: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.templates, Unset):
            templates = []
            for templates_item_data in self.templates:
                templates_item = templates_item_data.to_dict()
                templates.append(templates_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "created_at": created_at,
                "updated_at": updated_at,
                "created_by_user": created_by_user,
            }
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if num_log_records is not UNSET:
            field_dict["num_log_records"] = num_log_records
        if num_annotators is not UNSET:
            field_dict["num_annotators"] = num_annotators
        if num_users is not UNSET:
            field_dict["num_users"] = num_users
        if num_templates is not UNSET:
            field_dict["num_templates"] = num_templates
        if num_logs_annotated is not UNSET:
            field_dict["num_logs_annotated"] = num_logs_annotated
        if progress is not UNSET:
            field_dict["progress"] = progress
        if overall_progress is not UNSET:
            field_dict["overall_progress"] = overall_progress
        if templates is not UNSET:
            field_dict["templates"] = templates

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_queue_response_num_logs_annotated_type_0 import (
            AnnotationQueueResponseNumLogsAnnotatedType0,
        )
        from ..models.annotation_queue_response_progress_type_0 import AnnotationQueueResponseProgressType0
        from ..models.annotation_template_db import AnnotationTemplateDB
        from ..models.permission import Permission
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_created_by_user(data: object) -> None | UserInfo:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                created_by_user_type_0 = UserInfo.from_dict(data)

                return created_by_user_type_0
            except:  # noqa: E722
                pass
            return cast(None | UserInfo, data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user"))

        _permissions = d.pop("permissions", UNSET)
        permissions: list[Permission] | Unset = UNSET
        if _permissions is not UNSET:
            permissions = []
            for permissions_item_data in _permissions:
                permissions_item = Permission.from_dict(permissions_item_data)

                permissions.append(permissions_item)

        num_log_records = d.pop("num_log_records", UNSET)

        num_annotators = d.pop("num_annotators", UNSET)

        num_users = d.pop("num_users", UNSET)

        num_templates = d.pop("num_templates", UNSET)

        def _parse_num_logs_annotated(data: object) -> AnnotationQueueResponseNumLogsAnnotatedType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                num_logs_annotated_type_0 = AnnotationQueueResponseNumLogsAnnotatedType0.from_dict(data)

                return num_logs_annotated_type_0
            except:  # noqa: E722
                pass
            return cast(AnnotationQueueResponseNumLogsAnnotatedType0 | None | Unset, data)

        num_logs_annotated = _parse_num_logs_annotated(d.pop("num_logs_annotated", UNSET))

        def _parse_progress(data: object) -> AnnotationQueueResponseProgressType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                progress_type_0 = AnnotationQueueResponseProgressType0.from_dict(data)

                return progress_type_0
            except:  # noqa: E722
                pass
            return cast(AnnotationQueueResponseProgressType0 | None | Unset, data)

        progress = _parse_progress(d.pop("progress", UNSET))

        def _parse_overall_progress(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        overall_progress = _parse_overall_progress(d.pop("overall_progress", UNSET))

        _templates = d.pop("templates", UNSET)
        templates: list[AnnotationTemplateDB] | Unset = UNSET
        if _templates is not UNSET:
            templates = []
            for templates_item_data in _templates:
                templates_item = AnnotationTemplateDB.from_dict(templates_item_data)

                templates.append(templates_item)

        annotation_queue_response = cls(
            id=id,
            name=name,
            description=description,
            created_at=created_at,
            updated_at=updated_at,
            created_by_user=created_by_user,
            permissions=permissions,
            num_log_records=num_log_records,
            num_annotators=num_annotators,
            num_users=num_users,
            num_templates=num_templates,
            num_logs_annotated=num_logs_annotated,
            progress=progress,
            overall_progress=overall_progress,
            templates=templates,
        )

        annotation_queue_response.additional_properties = d
        return annotation_queue_response

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
