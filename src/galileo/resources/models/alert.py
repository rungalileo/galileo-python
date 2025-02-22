from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Alert")


@_attrs_define
class Alert:
    """
    Attributes:
        alert_message (str):
        alert_title (str):
    """

    alert_message: str
    alert_title: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alert_message = self.alert_message

        alert_title = self.alert_title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"alert_message": alert_message, "alert_title": alert_title})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        alert_message = d.pop("alert_message")

        alert_title = d.pop("alert_title")

        alert = cls(alert_message=alert_message, alert_title=alert_title)

        alert.additional_properties = d
        return alert

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
