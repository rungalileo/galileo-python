import datetime
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="RunTagDB")


@_attrs_define
class RunTagDB:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by (str):
        id (str):
        key (str):
        project_id (str):
        run_id (str):
        tag_type (str):
        updated_at (datetime.datetime):
        value (str):
    """

    created_at: datetime.datetime
    created_by: str
    id: str
    key: str
    project_id: str
    run_id: str
    tag_type: str
    updated_at: datetime.datetime
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        id = self.id

        key = self.key

        project_id = self.project_id

        run_id = self.run_id

        tag_type = self.tag_type

        updated_at = self.updated_at.isoformat()

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by": created_by,
                "id": id,
                "key": key,
                "project_id": project_id,
                "run_id": run_id,
                "tag_type": tag_type,
                "updated_at": updated_at,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        id = d.pop("id")

        key = d.pop("key")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        tag_type = d.pop("tag_type")

        updated_at = isoparse(d.pop("updated_at"))

        value = d.pop("value")

        run_tag_db = cls(
            created_at=created_at,
            created_by=created_by,
            id=id,
            key=key,
            project_id=project_id,
            run_id=run_id,
            tag_type=tag_type,
            updated_at=updated_at,
            value=value,
        )

        run_tag_db.additional_properties = d
        return run_tag_db

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
