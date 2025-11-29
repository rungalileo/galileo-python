import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="LogStreamResponse")


@_attrs_define
class LogStreamResponse:
    """
    Attributes
    ----------
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        name (str):
        project_id (str):
        created_by (Union[None, Unset, str]):
        created_by_user (Union['UserInfo', None, Unset]):
        num_spans (Union[None, Unset, int]):
        num_traces (Union[None, Unset, int]):
        has_user_created_sessions (Union[Unset, bool]):  Default: False.
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    project_id: str
    created_by: Union[None, Unset, str] = UNSET
    created_by_user: Union["UserInfo", None, Unset] = UNSET
    num_spans: Union[None, Unset, int] = UNSET
    num_traces: Union[None, Unset, int] = UNSET
    has_user_created_sessions: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_info import UserInfo

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        name = self.name

        project_id = self.project_id

        created_by: Union[None, Unset, str]
        created_by = UNSET if isinstance(self.created_by, Unset) else self.created_by

        created_by_user: Union[None, Unset, dict[str, Any]]
        if isinstance(self.created_by_user, Unset):
            created_by_user = UNSET
        elif isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        num_spans: Union[None, Unset, int]
        num_spans = UNSET if isinstance(self.num_spans, Unset) else self.num_spans

        num_traces: Union[None, Unset, int]
        num_traces = UNSET if isinstance(self.num_traces, Unset) else self.num_traces

        has_user_created_sessions = self.has_user_created_sessions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "created_at": created_at, "updated_at": updated_at, "name": name, "project_id": project_id}
        )
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if created_by_user is not UNSET:
            field_dict["created_by_user"] = created_by_user
        if num_spans is not UNSET:
            field_dict["num_spans"] = num_spans
        if num_traces is not UNSET:
            field_dict["num_traces"] = num_traces
        if has_user_created_sessions is not UNSET:
            field_dict["has_user_created_sessions"] = has_user_created_sessions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        name = d.pop("name")

        project_id = d.pop("project_id")

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_created_by_user(data: object) -> Union["UserInfo", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return UserInfo.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["UserInfo", None, Unset], data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user", UNSET))

        def _parse_num_spans(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_spans = _parse_num_spans(d.pop("num_spans", UNSET))

        def _parse_num_traces(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_traces = _parse_num_traces(d.pop("num_traces", UNSET))

        has_user_created_sessions = d.pop("has_user_created_sessions", UNSET)

        log_stream_response = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            project_id=project_id,
            created_by=created_by,
            created_by_user=created_by_user,
            num_spans=num_spans,
            num_traces=num_traces,
            has_user_created_sessions=has_user_created_sessions,
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
