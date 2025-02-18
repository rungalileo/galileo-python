from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.stage_type import StageType

T = TypeVar("T", bound="StageMetadata")


@_attrs_define
class StageMetadata:
    """
    Attributes:
        project_id (str):
        stage_id (str):
        stage_name (str):
        stage_type (StageType):
        stage_version (int):
    """

    project_id: str
    stage_id: str
    stage_name: str
    stage_type: StageType
    stage_version: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        stage_id = self.stage_id

        stage_name = self.stage_name

        stage_type = self.stage_type.value

        stage_version = self.stage_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "stage_id": stage_id,
                "stage_name": stage_name,
                "stage_type": stage_type,
                "stage_version": stage_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("project_id")

        stage_id = d.pop("stage_id")

        stage_name = d.pop("stage_name")

        stage_type = StageType(d.pop("stage_type"))

        stage_version = d.pop("stage_version")

        stage_metadata = cls(
            project_id=project_id,
            stage_id=stage_id,
            stage_name=stage_name,
            stage_type=stage_type,
            stage_version=stage_version,
        )

        stage_metadata.additional_properties = d
        return stage_metadata

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
