from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_stream_response import LogStreamResponse


T = TypeVar("T", bound="ListLogStreamResponse")


@_attrs_define
class ListLogStreamResponse:
    """
    Attributes
    ----------
        log_streams (list['LogStreamResponse']):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        paginated (Union[Unset, bool]):  Default: False.
        next_starting_token (Union[None, Unset, int]):
    """

    log_streams: list["LogStreamResponse"]
    starting_token: Union[Unset, int] = 0
    limit: Union[Unset, int] = 100
    paginated: Union[Unset, bool] = False
    next_starting_token: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        log_streams = []
        for log_streams_item_data in self.log_streams:
            log_streams_item = log_streams_item_data.to_dict()
            log_streams.append(log_streams_item)

        starting_token = self.starting_token

        limit = self.limit

        paginated = self.paginated

        next_starting_token: Union[None, Unset, int]
        next_starting_token = UNSET if isinstance(self.next_starting_token, Unset) else self.next_starting_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"log_streams": log_streams})
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if limit is not UNSET:
            field_dict["limit"] = limit
        if paginated is not UNSET:
            field_dict["paginated"] = paginated
        if next_starting_token is not UNSET:
            field_dict["next_starting_token"] = next_starting_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_stream_response import LogStreamResponse

        d = dict(src_dict)
        log_streams = []
        _log_streams = d.pop("log_streams")
        for log_streams_item_data in _log_streams:
            log_streams_item = LogStreamResponse.from_dict(log_streams_item_data)

            log_streams.append(log_streams_item)

        starting_token = d.pop("starting_token", UNSET)

        limit = d.pop("limit", UNSET)

        paginated = d.pop("paginated", UNSET)

        def _parse_next_starting_token(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        next_starting_token = _parse_next_starting_token(d.pop("next_starting_token", UNSET))

        list_log_stream_response = cls(
            log_streams=log_streams,
            starting_token=starting_token,
            limit=limit,
            paginated=paginated,
            next_starting_token=next_starting_token,
        )

        list_log_stream_response.additional_properties = d
        return list_log_stream_response

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
