from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.token_usage import TokenUsage


T = TypeVar("T", bound="LogStreamInsightTokenUsageDB")


@_attrs_define
class LogStreamInsightTokenUsageDB:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        project_id (str):
        log_stream_id (str):
        token_usage (TokenUsage | Unset): Token usage information for insights generation.
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    project_id: str
    log_stream_id: str
    token_usage: TokenUsage | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        project_id = self.project_id

        log_stream_id = self.log_stream_id

        token_usage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.token_usage, Unset):
            token_usage = self.token_usage.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "project_id": project_id,
                "log_stream_id": log_stream_id,
            }
        )
        if token_usage is not UNSET:
            field_dict["token_usage"] = token_usage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.token_usage import TokenUsage

        d = dict(src_dict)
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        project_id = d.pop("project_id")

        log_stream_id = d.pop("log_stream_id")

        _token_usage = d.pop("token_usage", UNSET)
        token_usage: TokenUsage | Unset
        if isinstance(_token_usage, Unset):
            token_usage = UNSET
        else:
            token_usage = TokenUsage.from_dict(_token_usage)

        log_stream_insight_token_usage_db = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            project_id=project_id,
            log_stream_id=log_stream_id,
            token_usage=token_usage,
        )

        log_stream_insight_token_usage_db.additional_properties = d
        return log_stream_insight_token_usage_db

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
