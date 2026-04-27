from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.component_type import ComponentType
from ..models.view_visibility import ViewVisibility
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component_view_response_view_data import ComponentViewResponseViewData


T = TypeVar("T", bound="ComponentViewResponse")


@_attrs_define
class ComponentViewResponse:
    """Response schema for component view with computed fields.

    Attributes:
        id (str):
        created_by (str):
        project_id (str):
        run_id (None | str):
        component (ComponentType): Types of components that can have saved views.
        visibility (ViewVisibility): Visibility levels for views.
        name (str):
        description (None | str):
        view_data (ComponentViewResponseViewData):
        is_default (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        can_edit (bool | Unset):  Default: False.
    """

    id: str
    created_by: str
    project_id: str
    run_id: None | str
    component: ComponentType
    visibility: ViewVisibility
    name: str
    description: None | str
    view_data: ComponentViewResponseViewData
    is_default: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    can_edit: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_by = self.created_by

        project_id = self.project_id

        run_id: None | str
        run_id = self.run_id

        component = self.component.value

        visibility = self.visibility.value

        name = self.name

        description: None | str
        description = self.description

        view_data = self.view_data.to_dict()

        is_default = self.is_default

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        can_edit = self.can_edit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_by": created_by,
                "project_id": project_id,
                "run_id": run_id,
                "component": component,
                "visibility": visibility,
                "name": name,
                "description": description,
                "view_data": view_data,
                "is_default": is_default,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if can_edit is not UNSET:
            field_dict["can_edit"] = can_edit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_view_response_view_data import ComponentViewResponseViewData

        d = dict(src_dict)
        id = d.pop("id")

        created_by = d.pop("created_by")

        project_id = d.pop("project_id")

        def _parse_run_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        run_id = _parse_run_id(d.pop("run_id"))

        component = ComponentType(d.pop("component"))

        visibility = ViewVisibility(d.pop("visibility"))

        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        view_data = ComponentViewResponseViewData.from_dict(d.pop("view_data"))

        is_default = d.pop("is_default")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        can_edit = d.pop("can_edit", UNSET)

        component_view_response = cls(
            id=id,
            created_by=created_by,
            project_id=project_id,
            run_id=run_id,
            component=component,
            visibility=visibility,
            name=name,
            description=description,
            view_data=view_data,
            is_default=is_default,
            created_at=created_at,
            updated_at=updated_at,
            can_edit=can_edit,
        )

        component_view_response.additional_properties = d
        return component_view_response

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
