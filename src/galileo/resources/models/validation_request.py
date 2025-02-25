from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ValidationRequest")


@_attrs_define
class ValidationRequest:
    """
    Attributes:
        payload (str):
        file_type (Union[Unset, str]):  Default: 'csv'.
    """

    payload: str
    file_type: Union[Unset, str] = "csv"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = self.payload

        file_type = self.file_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"payload": payload})
        if file_type is not UNSET:
            field_dict["file_type"] = file_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        payload = d.pop("payload")

        file_type = d.pop("file_type", UNSET)

        validation_request = cls(payload=payload, file_type=file_type)

        validation_request.additional_properties = d
        return validation_request

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
