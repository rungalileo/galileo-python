from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component_view_update_view_data_type_0 import ComponentViewUpdateViewDataType0


T = TypeVar("T", bound="ComponentViewUpdate")


@_attrs_define
class ComponentViewUpdate:
    """Schema for updating an existing component view.

    Attributes:
        name (None | str | Unset):
        description (None | str | Unset):
        view_data (ComponentViewUpdateViewDataType0 | None | Unset):
    """

    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    view_data: ComponentViewUpdateViewDataType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.component_view_update_view_data_type_0 import ComponentViewUpdateViewDataType0

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        view_data: dict[str, Any] | None | Unset
        if isinstance(self.view_data, Unset):
            view_data = UNSET
        elif isinstance(self.view_data, ComponentViewUpdateViewDataType0):
            view_data = self.view_data.to_dict()
        else:
            view_data = self.view_data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if view_data is not UNSET:
            field_dict["view_data"] = view_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_view_update_view_data_type_0 import ComponentViewUpdateViewDataType0

        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_view_data(data: object) -> ComponentViewUpdateViewDataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                view_data_type_0 = ComponentViewUpdateViewDataType0.from_dict(data)

                return view_data_type_0
            except:  # noqa: E722
                pass
            return cast(ComponentViewUpdateViewDataType0 | None | Unset, data)

        view_data = _parse_view_data(d.pop("view_data", UNSET))

        component_view_update = cls(name=name, description=description, view_data=view_data)

        component_view_update.additional_properties = d
        return component_view_update

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
