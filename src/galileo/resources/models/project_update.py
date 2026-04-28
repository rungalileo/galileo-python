from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.project_type import ProjectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectUpdate")


@_attrs_define
class ProjectUpdate:
    """
    Attributes
    ----------
        name (None | str | Unset):
        created_by (None | str | Unset):
        type_ (None | ProjectType | Unset):
        labels (list[str] | None | Unset):
        description (None | str | Unset):
    """

    name: None | str | Unset = UNSET
    created_by: None | str | Unset = UNSET
    type_: None | ProjectType | Unset = UNSET
    labels: list[str] | None | Unset = UNSET
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: None | str | Unset
        name = UNSET if isinstance(self.name, Unset) else self.name

        created_by: None | str | Unset
        created_by = UNSET if isinstance(self.created_by, Unset) else self.created_by

        type_: None | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        elif isinstance(self.type_, ProjectType):
            type_ = self.type_.value
        else:
            type_ = self.type_

        labels: list[str] | None | Unset
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, list):
            labels = self.labels

        else:
            labels = self.labels

        description: None | str | Unset
        description = UNSET if isinstance(self.description, Unset) else self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if type_ is not UNSET:
            field_dict["type"] = type_
        if labels is not UNSET:
            field_dict["labels"] = labels
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_created_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_type_(data: object) -> None | ProjectType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ProjectType(data)

            except:  # noqa: E722
                pass
            return cast(None | ProjectType | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_labels(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        labels = _parse_labels(d.pop("labels", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        project_update = cls(name=name, created_by=created_by, type_=type_, labels=labels, description=description)

        project_update.additional_properties = d
        return project_update

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
