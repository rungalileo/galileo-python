import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.project_type import ProjectType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission
    from ..models.run_db_thin import RunDBThin


T = TypeVar("T", bound="ProjectDBThin")


@_attrs_define
class ProjectDBThin:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by (str):
        id (str):
        runs (list['RunDBThin']):
        updated_at (datetime.datetime):
        bookmark (Union[Unset, bool]):  Default: False.
        name (Union[None, Unset, str]):
        permissions (Union[Unset, list['Permission']]):
        type_ (Union[None, ProjectType, Unset]):
    """

    created_at: datetime.datetime
    created_by: str
    id: str
    runs: list["RunDBThin"]
    updated_at: datetime.datetime
    bookmark: Union[Unset, bool] = False
    name: Union[None, Unset, str] = UNSET
    permissions: Union[Unset, list["Permission"]] = UNSET
    type_: Union[None, ProjectType, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        id = self.id

        runs = []
        for runs_item_data in self.runs:
            runs_item = runs_item_data.to_dict()
            runs.append(runs_item)

        updated_at = self.updated_at.isoformat()

        bookmark = self.bookmark

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        permissions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        elif isinstance(self.type_, ProjectType):
            type_ = self.type_.value
        else:
            type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"created_at": created_at, "created_by": created_by, "id": id, "runs": runs, "updated_at": updated_at}
        )
        if bookmark is not UNSET:
            field_dict["bookmark"] = bookmark
        if name is not UNSET:
            field_dict["name"] = name
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.permission import Permission
        from ..models.run_db_thin import RunDBThin

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        id = d.pop("id")

        runs = []
        _runs = d.pop("runs")
        for runs_item_data in _runs:
            runs_item = RunDBThin.from_dict(runs_item_data)

            runs.append(runs_item)

        updated_at = isoparse(d.pop("updated_at"))

        bookmark = d.pop("bookmark", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        def _parse_type_(data: object) -> Union[None, ProjectType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_0 = ProjectType(data)

                return type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ProjectType, Unset], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        project_db_thin = cls(
            created_at=created_at,
            created_by=created_by,
            id=id,
            runs=runs,
            updated_at=updated_at,
            bookmark=bookmark,
            name=name,
            permissions=permissions,
            type_=type_,
        )

        project_db_thin.additional_properties = d
        return project_db_thin

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
