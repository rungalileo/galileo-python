from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChatWithMetricRequest")


@_attrs_define
class ChatWithMetricRequest:
    """
    Attributes:
        project_id (str):
        log_stream_id (str):
        metric_name (str):
        chat_query (None | str | Unset):
        is_restart (bool | None | Unset):  Default: False.
    """

    project_id: str
    log_stream_id: str
    metric_name: str
    chat_query: None | str | Unset = UNSET
    is_restart: bool | None | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        log_stream_id = self.log_stream_id

        metric_name = self.metric_name

        chat_query: None | str | Unset
        if isinstance(self.chat_query, Unset):
            chat_query = UNSET
        else:
            chat_query = self.chat_query

        is_restart: bool | None | Unset
        if isinstance(self.is_restart, Unset):
            is_restart = UNSET
        else:
            is_restart = self.is_restart

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "log_stream_id": log_stream_id, "metric_name": metric_name})
        if chat_query is not UNSET:
            field_dict["chat_query"] = chat_query
        if is_restart is not UNSET:
            field_dict["is_restart"] = is_restart

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        log_stream_id = d.pop("log_stream_id")

        metric_name = d.pop("metric_name")

        def _parse_chat_query(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        chat_query = _parse_chat_query(d.pop("chat_query", UNSET))

        def _parse_is_restart(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_restart = _parse_is_restart(d.pop("is_restart", UNSET))

        chat_with_metric_request = cls(
            project_id=project_id,
            log_stream_id=log_stream_id,
            metric_name=metric_name,
            chat_query=chat_query,
            is_restart=is_restart,
        )

        chat_with_metric_request.additional_properties = d
        return chat_with_metric_request

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
