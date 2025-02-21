import datetime
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.integration_name import IntegrationName

T = TypeVar("T", bound="IntegrationDB")


@_attrs_define
class IntegrationDB:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by (str):
        id (str):
        name (IntegrationName):
        updated_at (datetime.datetime):
    """

    created_at: datetime.datetime
    created_by: str
    id: str
    name: IntegrationName
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        id = self.id

        name = self.name.value

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"created_at": created_at, "created_by": created_by, "id": id, "name": name, "updated_at": updated_at}
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        id = d.pop("id")

        name = IntegrationName(d.pop("name"))

        updated_at = isoparse(d.pop("updated_at"))

        integration_db = cls(created_at=created_at, created_by=created_by, id=id, name=name, updated_at=updated_at)

        integration_db.additional_properties = d
        return integration_db

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
