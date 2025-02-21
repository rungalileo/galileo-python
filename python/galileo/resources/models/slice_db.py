import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="SliceDB")


@_attrs_define
class SliceDB:
    """
    Attributes:
        created_at (datetime.datetime):
        id (str):
        logic (FilterParams):
        name (str):
        updated_at (datetime.datetime):
        created_by (Union[None, Unset, str]):
        project_id (Union[None, Unset, str]):
    """

    created_at: datetime.datetime
    id: str
    logic: "FilterParams"
    name: str
    updated_at: datetime.datetime
    created_by: Union[None, Unset, str] = UNSET
    project_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        logic = self.logic.to_dict()

        name = self.name

        updated_at = self.updated_at.isoformat()

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"created_at": created_at, "id": id, "logic": logic, "name": name, "updated_at": updated_at})
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_params import FilterParams

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        logic = FilterParams.from_dict(d.pop("logic"))

        name = d.pop("name")

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_project_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        slice_db = cls(
            created_at=created_at,
            id=id,
            logic=logic,
            name=name,
            updated_at=updated_at,
            created_by=created_by,
            project_id=project_id,
        )

        slice_db.additional_properties = d
        return slice_db

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
