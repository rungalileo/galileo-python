from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
        status (Union[Unset, Any]): Status of the request after processing the rules. Default: 'not_triggered'.
    """

    text: str
    trace_metadata: "TraceMetadata"
    status: Union[Unset, Any] = "not_triggered"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        trace_metadata = self.trace_metadata.to_dict()

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"text": text, "trace_metadata": trace_metadata})
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.trace_metadata import TraceMetadata

        d = src_dict.copy()
        text = d.pop("text")

        trace_metadata = TraceMetadata.from_dict(d.pop("trace_metadata"))

        status = d.pop("status", UNSET)

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
