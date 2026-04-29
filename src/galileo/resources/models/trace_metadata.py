from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TraceMetadata")


@_attrs_define
class TraceMetadata:
    """
    Attributes
    ----------
        id (Union[Unset, str]): Unique identifier for the request.
        received_at (Union[Unset, int]): Time the request was received by the server in nanoseconds.
        response_at (Union[Unset, int]): Time the response was sent by the server in nanoseconds.
        execution_time (Union[Unset, float]): Execution time for the request (in seconds). Default: -1.0.
    """

    id: Union[Unset, str] = UNSET
    received_at: Union[Unset, int] = UNSET
    response_at: Union[Unset, int] = UNSET
    execution_time: Union[Unset, float] = -1.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        received_at = self.received_at

        response_at = self.response_at

        execution_time = self.execution_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if received_at is not UNSET:
            field_dict["received_at"] = received_at
        if response_at is not UNSET:
            field_dict["response_at"] = response_at
        if execution_time is not UNSET:
            field_dict["execution_time"] = execution_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        received_at = d.pop("received_at", UNSET)

        response_at = d.pop("response_at", UNSET)

        execution_time = d.pop("execution_time", UNSET)

        trace_metadata = cls(id=id, received_at=received_at, response_at=response_at, execution_time=execution_time)

        trace_metadata.additional_properties = d
        return trace_metadata

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
