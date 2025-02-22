from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StageDB")


@_attrs_define
class StageDB:
    """
    Attributes:
        created_by (str):
        id (str):
        name (str): Name of the stage. Must be unique within the project.
        project_id (str): ID of the project to which this stage belongs.
        description (Union[None, Unset, str]): Optional human-readable description of the goals of this guardrail.
        paused (Union[Unset, bool]): Whether the action is enabled. If False, the action will not be applied. Default:
            False.
        type_ (Union[Unset, Any]): Type of the stage. Default: 'local'.
        version (Union[None, Unset, int]):
    """

    created_by: str
    id: str
    name: str
    project_id: str
    description: Union[None, Unset, str] = UNSET
    paused: Union[Unset, bool] = False
    type_: Union[Unset, Any] = "local"
    version: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_by = self.created_by

        id = self.id

        name = self.name

        project_id = self.project_id

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        paused = self.paused

        type_ = self.type_

        version: Union[None, Unset, int]
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"created_by": created_by, "id": id, "name": name, "project_id": project_id})
        if description is not UNSET:
            field_dict["description"] = description
        if paused is not UNSET:
            field_dict["paused"] = paused
        if type_ is not UNSET:
            field_dict["type"] = type_
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created_by = d.pop("created_by")

        id = d.pop("id")

        name = d.pop("name")

        project_id = d.pop("project_id")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        paused = d.pop("paused", UNSET)

        type_ = d.pop("type", UNSET)

        def _parse_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        version = _parse_version(d.pop("version", UNSET))

        stage_db = cls(
            created_by=created_by,
            id=id,
            name=name,
            project_id=project_id,
            description=description,
            paused=paused,
            type_=type_,
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
