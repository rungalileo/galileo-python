from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.component_type import ComponentType
from ..models.view_visibility import ViewVisibility
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component_view_create_view_data import ComponentViewCreateViewData


T = TypeVar("T", bound="ComponentViewCreate")


@_attrs_define
class ComponentViewCreate:
    """Schema for creating a new component view.

    Attributes:
        project_id (str):
        component (ComponentType): Types of components that can have saved views.
        name (str): Name of the view
        view_data (ComponentViewCreateViewData): JSON view configuration
        run_id (None | str | Unset):
        visibility (ViewVisibility | Unset): Visibility levels for views.
        description (None | str | Unset): Optional description
    """

    project_id: str
    component: ComponentType
    name: str
    view_data: ComponentViewCreateViewData
    run_id: None | str | Unset = UNSET
    visibility: ViewVisibility | Unset = UNSET
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        component = self.component.value

        name = self.name

        view_data = self.view_data.to_dict()

        run_id: None | str | Unset
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        else:
            run_id = self.run_id

        visibility: str | Unset = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "component": component, "name": name, "view_data": view_data})
        if run_id is not UNSET:
            field_dict["run_id"] = run_id
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_view_create_view_data import ComponentViewCreateViewData

        d = dict(src_dict)
        project_id = d.pop("project_id")

        component = ComponentType(d.pop("component"))

        name = d.pop("name")

        view_data = ComponentViewCreateViewData.from_dict(d.pop("view_data"))

        def _parse_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        _visibility = d.pop("visibility", UNSET)
        visibility: ViewVisibility | Unset
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = ViewVisibility(_visibility)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        component_view_create = cls(
            project_id=project_id,
            component=component,
            name=name,
            view_data=view_data,
            run_id=run_id,
            visibility=visibility,
            description=description,
        )

        component_view_create.additional_properties = d
        return component_view_create

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
