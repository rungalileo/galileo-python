from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_status import ExecutionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionConfig")


@_attrs_define
class SubscriptionConfig:
    """
    Attributes:
        url (str): URL to send the event to. This can be a webhook URL, a message queue URL, an event bus or a custom
            endpoint that can receive an HTTP POST request.
        statuses (Union[Unset, list[ExecutionStatus]]): List of statuses that will cause a notification to be sent to
            the configured URL.
    """

    url: str
    statuses: Union[Unset, list[ExecutionStatus]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        statuses: Union[Unset, list[str]] = UNSET
        if not isinstance(self.statuses, Unset):
            statuses = []
            for statuses_item_data in self.statuses:
                statuses_item = statuses_item_data.value
                statuses.append(statuses_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"url": url})
        if statuses is not UNSET:
            field_dict["statuses"] = statuses

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        statuses = []
        _statuses = d.pop("statuses", UNSET)
        for statuses_item_data in _statuses or []:
            statuses_item = ExecutionStatus(statuses_item_data)

            statuses.append(statuses_item)

        subscription_config = cls(url=url, statuses=statuses)

        subscription_config.additional_properties = d
        return subscription_config

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
