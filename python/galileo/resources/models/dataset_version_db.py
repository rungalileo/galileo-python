import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="DatasetVersionDB")


@_attrs_define
class DatasetVersionDB:
    """
    Attributes:
        column_names (list[str]):
        columns_added (int):
        columns_removed (int):
        columns_renamed (int):
        created_at (datetime.datetime):
        created_by_user (Union['UserInfo', None]):
        name (Union[None, str]):
        num_rows (int):
        rows_added (int):
        rows_edited (int):
        rows_removed (int):
        version_index (int):
    """

    column_names: list[str]
    columns_added: int
    columns_removed: int
    columns_renamed: int
    created_at: datetime.datetime
    created_by_user: Union["UserInfo", None]
    name: Union[None, str]
    num_rows: int
    rows_added: int
    rows_edited: int
    rows_removed: int
    version_index: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_info import UserInfo

        column_names = self.column_names

        columns_added = self.columns_added

        columns_removed = self.columns_removed

        columns_renamed = self.columns_renamed

        created_at = self.created_at.isoformat()

        created_by_user: Union[None, dict[str, Any]]
        if isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        name: Union[None, str]
        name = self.name

        num_rows = self.num_rows

        rows_added = self.rows_added

        rows_edited = self.rows_edited

        rows_removed = self.rows_removed

        version_index = self.version_index

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "column_names": column_names,
                "columns_added": columns_added,
                "columns_removed": columns_removed,
                "columns_renamed": columns_renamed,
                "created_at": created_at,
                "created_by_user": created_by_user,
                "name": name,
                "num_rows": num_rows,
                "rows_added": rows_added,
                "rows_edited": rows_edited,
                "rows_removed": rows_removed,
                "version_index": version_index,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.user_info import UserInfo

        d = src_dict.copy()
        column_names = cast(list[str], d.pop("column_names"))

        columns_added = d.pop("columns_added")

        columns_removed = d.pop("columns_removed")

        columns_renamed = d.pop("columns_renamed")

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

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        num_rows = d.pop("num_rows")

        rows_added = d.pop("rows_added")

        rows_edited = d.pop("rows_edited")

        rows_removed = d.pop("rows_removed")

        version_index = d.pop("version_index")

        dataset_version_db = cls(
            column_names=column_names,
            columns_added=columns_added,
            columns_removed=columns_removed,
            columns_renamed=columns_renamed,
            created_at=created_at,
            created_by_user=created_by_user,
            name=name,
            num_rows=num_rows,
            rows_added=rows_added,
            rows_edited=rows_edited,
            rows_removed=rows_removed,
            version_index=version_index,
        )

        dataset_version_db.additional_properties = d
        return dataset_version_db

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
