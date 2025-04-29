import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogStreamResponse")


@_attrs_define
class LogStreamResponse:
    """
    Attributes:
        created_at (datetime.datetime):
        id (str):
        name (str):
        project_id (str):
        updated_at (datetime.datetime):
        created_by (Union[None, Unset, str]):
    """

    created_at: datetime.datetime
    id: str
    name: str
    project_id: str
    updated_at: datetime.datetime
    created_by: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        name = self.name

        project_id = self.project_id

        updated_at = self.updated_at.isoformat()

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"created_at": created_at, "id": id, "name": name, "project_id": project_id, "updated_at": updated_at}
        )
        if created_by is not UNSET:
            field_dict["created_by"] = created_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        name = d.pop("name")

        project_id = d.pop("project_id")

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        log_stream_response = cls(
            created_at=created_at, id=id, name=name, project_id=project_id, updated_at=updated_at, created_by=created_by
        )

        log_stream_response.additional_properties = d
        return log_stream_response

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
