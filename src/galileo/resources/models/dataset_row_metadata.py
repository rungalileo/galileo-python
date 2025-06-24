import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="DatasetRowMetadata")


@_attrs_define
class DatasetRowMetadata:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by_user (Union['UserInfo', None]):
        created_in_version (int):
        updated_at (datetime.datetime):
        updated_by_user (Union['UserInfo', None]):
        updated_in_version (int):
    """

    created_at: datetime.datetime
    created_by_user: Union["UserInfo", None]
    created_in_version: int
    updated_at: datetime.datetime
    updated_by_user: Union["UserInfo", None]
    updated_in_version: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_info import UserInfo

        created_at = self.created_at.isoformat()

        created_by_user: Union[None, dict[str, Any]]
        if isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        created_in_version = self.created_in_version

        updated_at = self.updated_at.isoformat()

        updated_by_user: Union[None, dict[str, Any]]
        if isinstance(self.updated_by_user, UserInfo):
            updated_by_user = self.updated_by_user.to_dict()
        else:
            updated_by_user = self.updated_by_user

        updated_in_version = self.updated_in_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by_user": created_by_user,
                "created_in_version": created_in_version,
                "updated_at": updated_at,
                "updated_by_user": updated_by_user,
                "updated_in_version": updated_in_version,
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

        created_in_version = d.pop("created_in_version")

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_updated_by_user(data: object) -> Union["UserInfo", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                updated_by_user_type_0 = UserInfo.from_dict(data)

                return updated_by_user_type_0
            except:  # noqa: E722
                pass
            return cast(Union["UserInfo", None], data)

        updated_by_user = _parse_updated_by_user(d.pop("updated_by_user"))

        updated_in_version = d.pop("updated_in_version")

        dataset_row_metadata = cls(
            created_at=created_at,
            created_by_user=created_by_user,
            created_in_version=created_in_version,
            updated_at=updated_at,
            updated_by_user=updated_by_user,
            updated_in_version=updated_in_version,
        )

        dataset_row_metadata.additional_properties = d
        return dataset_row_metadata

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
