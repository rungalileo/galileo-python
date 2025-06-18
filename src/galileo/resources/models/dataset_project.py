import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="DatasetProject")


@_attrs_define
class DatasetProject:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by_user (Union['UserInfo', None]):
        id (str):
        name (str):
        updated_at (datetime.datetime):
    """

    created_at: datetime.datetime
    created_by_user: Union["UserInfo", None]
    id: str
    name: str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_info import UserInfo

        created_at = self.created_at.isoformat()

        created_by_user: Union[None, dict[str, Any]]
        if isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        id = self.id

        name = self.name

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by_user": created_by_user,
                "id": id,
                "name": name,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        def _parse_created_by_user(data: object) -> Union["UserInfo", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                created_by_user_type_0 = UserInfo.from_dict(data)

                return created_by_user_type_0
            except:  # noqa: E722
                pass
            return cast(Union["UserInfo", None], data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user"))

        id = d.pop("id")

        name = d.pop("name")

        updated_at = isoparse(d.pop("updated_at"))

        dataset_project = cls(
            created_at=created_at, created_by_user=created_by_user, id=id, name=name, updated_at=updated_at
        )

        dataset_project.additional_properties = d
        return dataset_project

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
