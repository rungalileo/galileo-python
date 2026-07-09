from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.stage_type import StageType
from ..types import UNSET, Unset

T = TypeVar("T", bound="StageDB")


@_attrs_define
class StageDB:
    """
    Attributes:
        name (str): Name of the stage. Must be unique within the project.
        project_id (str): ID of the project to which this stage belongs.
        created_by (str):
        id (str):
        description (None | str | Unset): Optional human-readable description of the goals of this guardrail.
        type_ (StageType | Unset):
        paused (bool | Unset): Whether the action is enabled. If False, the action will not be applied. Default: False.
        version (int | None | Unset):
    """

    name: str
    project_id: str
    created_by: str
    id: str
    description: None | str | Unset = UNSET
    type_: StageType | Unset = UNSET
    paused: bool | Unset = False
    version: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        project_id = self.project_id

        created_by = self.created_by

        id = self.id

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        paused = self.paused

        version: int | None | Unset
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "project_id": project_id, "created_by": created_by, "id": id})
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_
        if paused is not UNSET:
            field_dict["paused"] = paused
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        project_id = d.pop("project_id")

        created_by = d.pop("created_by")

        id = d.pop("id")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: StageType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = StageType(_type_)

        paused = d.pop("paused", UNSET)

        def _parse_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        version = _parse_version(d.pop("version", UNSET))

        stage_db = cls(
            name=name,
            project_id=project_id,
            created_by=created_by,
            id=id,
            description=description,
            type_=type_,
            paused=paused,
            version=version,
        )

        stage_db.additional_properties = d
        return stage_db

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
