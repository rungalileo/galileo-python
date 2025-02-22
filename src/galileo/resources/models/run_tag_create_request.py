from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RunTagCreateRequest")


@_attrs_define
class RunTagCreateRequest:
    """
    Attributes:
        key (str):
        tag_type (str):
        value (str):
    """

    key: str
    tag_type: str
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        tag_type = self.tag_type

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"key": key, "tag_type": tag_type, "value": value})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        tag_type = d.pop("tag_type")

        value = d.pop("value")

        run_tag_create_request = cls(key=key, tag_type=tag_type, value=value)

        run_tag_create_request.additional_properties = d
        return run_tag_create_request

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
