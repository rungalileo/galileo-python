from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_status import ExecutionStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trace_metadata import TraceMetadata


T = TypeVar("T", bound="Response")


@_attrs_define
class Response:
    """
    Attributes:
        text (str): Text from the request after processing the rules.
        trace_metadata (TraceMetadata):
        status (Union[Unset, ExecutionStatus]): Status of the execution.
    """

    text: str
    trace_metadata: "TraceMetadata"
    status: Union[Unset, ExecutionStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        trace_metadata = self.trace_metadata.to_dict()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"text": text, "trace_metadata": trace_metadata})
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trace_metadata import TraceMetadata

        d = dict(src_dict)
        text = d.pop("text")

        trace_metadata = TraceMetadata.from_dict(d.pop("trace_metadata"))

        _status = d.pop("status", UNSET)
        status: Union[Unset, ExecutionStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ExecutionStatus(_status)

        response = cls(text=text, trace_metadata=trace_metadata, status=status)

        response.additional_properties = d
        return response

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
