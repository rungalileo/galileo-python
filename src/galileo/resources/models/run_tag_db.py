import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="RunTagDB")


@_attrs_define
class RunTagDB:
    """
    Attributes
    ----------
        key (str):
        value (str):
        tag_type (str):
        project_id (str):
        run_id (str):
        created_by (str):
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    key: str
    value: str
    tag_type: str
    project_id: str
    run_id: str
    created_by: str
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        value = self.value

        tag_type = self.tag_type

        project_id = self.project_id

        run_id = self.run_id

        created_by = self.created_by

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "value": value,
                "tag_type": tag_type,
                "project_id": project_id,
                "run_id": run_id,
                "created_by": created_by,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        value = d.pop("value")

        tag_type = d.pop("tag_type")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        created_by = d.pop("created_by")

        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        run_tag_db = cls(
            key=key,
            value=value,
            tag_type=tag_type,
            project_id=project_id,
            run_id=run_id,
            created_by=created_by,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
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
